"""
Order Executor Service

Responsible for processing orders from the order queue. 

Implements a leader election mechanism to ensure mutual exclusion, which is important as
this service is replicated several times. 
Docker API is used to identify all the replicas.

The leader dequeues orders from the queue (in Order Queue Service) and processes them. Other replicas
periodically check if the leader is up and if not, start a new election.

"""
import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb'))
sys.path.insert(0, grpc_path)

import common_pb2 as common
from concurrent import futures
import grpc
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc
import books_database_pb2 as books_database
import books_database_pb2_grpc as books_database_grpc
import docker
import time


class OrderExecutorService:
    def __init__(self, executor_id, known_ids):
        self.executor_id = executor_id
        self.known_ids = known_ids
        self.leader_id = None
    
    def send_declare_election(self, target_id: str):
        # Returns True if target is alive, False otherwise
        with grpc.insecure_channel(f'{target_id}:50051') as leader_channel:
            leader_election_stub = order_queue_grpc.LeaderElectionServiceStub(leader_channel)
            try:
                leader_election_stub.DeclareElection(order_queue.LeaderRequest(sender_id=self.executor_id), timeout=1)
                return True
            except Exception as e:
                return False
    
    def send_declare_victory(self, target_id: str):
        # Returns True if target is alive, False otherwise
        with grpc.insecure_channel(f'{target_id}:50051') as leader_channel:
            leader_election_stub = order_queue_grpc.LeaderElectionServiceStub(leader_channel)
            try:
                leader_election_stub.DeclareVictory(order_queue.LeaderRequest(sender_id=self.executor_id), timeout=1)
                return True
            except Exception:
                return False

    def start_leader_election(self):
        print(f"STARTING ELECTION: {self.executor_id} (known_ids = {self.known_ids})")
        for id in self.known_ids:
            if id > self.executor_id and self.send_declare_election(id):
                # A service with bigger id is alive, stop election
                print(f"ELECTION FAILED ({id} is alive)")
                # Consider the found service leader for now
                self.leader_id = id
                break
        else:
            # I am service with biggest id, declare victory
            print(f"DECLARING VICTORY: {self.executor_id}")
            self.leader_id = self.executor_id
            for id in self.known_ids:
                self.send_declare_victory(id)
    
    def execute_order(self, title, quantity, db_stub):
        #Read current stock
        response = db_stub.Read(books_database.ReadRequest(title=title))
        current_stock = response.stock

        #Check that enough books in stock
        if current_stock >= quantity:
            new_stock = current_stock - quantity
            write_response = db_stub.Write(books_database.WriteRequest(
                title=title,
                new_stock=new_stock
            ))
            return write_response.success
        return False #Too few in stock 
    
    def run(self):
        with grpc.insecure_channel('order_queue:50051') as order_queue_channel:
            order_queue_stub = order_queue_grpc.OrderQueueServiceStub(order_queue_channel)
            
            while True:
                if self.leader_id == self.executor_id:
                    # Is leader
                    
                    try:
                        order: common.ItemsInitRequest = order_queue_stub.Dequeue(common.Empty())
                    except grpc.RpcError as err:
                        if err.code() == grpc.StatusCode.ABORTED: # type: ignore
                            continue # Queue empty
                        else:
                            raise
                    
                    print("PROCESSING ORDER:", str(order).replace('\n', ' '))
                    # Process order here
                    with grpc.insecure_channel(f'books_database:50051') as db_channel:
                        db_stub = books_database_grpc.BooksDatabaseStub(db_channel)
                        for item in order.items:
                            if not self.execute_order(item.name, item.quantity, db_stub):
                                print(f"WARNING: Order for {item.quantity} copies of {item.name} failed, not enough stock")
                else:
                    # Is not leader
                    
                    if self.leader_id is not None:
                        # Ping leader using election declaration
                        if not self.send_declare_election(self.leader_id):
                            # Leader has failed, start new election
                            print(f"LEADER {self.leader_id} FAILED")
                            self.start_leader_election()

                    time.sleep(2)

class LeaderElectionService(order_queue_grpc.LeaderElectionServiceServicer):
    def __init__(self, svc: OrderExecutorService):
        self.svc = svc
    
    def DeclareElection(self, request: order_queue.LeaderRequest, context):
        # We are alive, respond to declaration
        return common.Empty()

    def DeclareVictory(self, request: order_queue.LeaderRequest, context):
        # New leader, update leader ID
        print(f"NEW LEADER: {request.sender_id}")
        self.svc.leader_id = request.sender_id
        return common.Empty()

def get_all_executor_ids():
    client = docker.from_env()
    
    executor_id = os.getenv('HOSTNAME', '')

    known_ids = []
    for container in client.containers.list(all=True):
        if container.labels.get('com.docker.compose.service') == 'order_executor':
            known_ids.append(container.short_id)

    assert executor_id in known_ids
    return executor_id, known_ids

def run():
    executor_id, known_ids = get_all_executor_ids()

    svc = OrderExecutorService(executor_id, known_ids)

    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    order_queue_grpc.add_LeaderElectionServiceServicer_to_server(LeaderElectionService(svc), server)
    # Listen on port 50051
    server.add_insecure_port("[::]:50051")
    # Start the server
    server.start()
    
    svc.start_leader_election()
    svc.run()

if __name__ == '__main__':
    run()
