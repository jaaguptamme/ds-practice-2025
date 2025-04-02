import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb'))
sys.path.insert(0, grpc_path)
import common_pb2 as common
import threading
from concurrent import futures
import grpc
import order_queue_pb2_grpc as order_queue_grpc
import docker
import time
class OrderExecutorService:
    def __init__(self, executor_id, known_ids, queue_stub):
        self.executor_id = executor_id
        self.know_ids=known_ids
        self.queue_stub=queue_stub
        self.leader_id = None 
    def start_leader_election(self):
        #TODO
        print("STARTING",self.executor_id)
        pass 
    def run(self):
        #TODO
        print("RUNNING",self.executor_id)
        while True:
            time.sleep(10)
            print("RUNNING")
        pass
    
def launch_executor(executor_id, know_ids):
    # Create a gRPC server
    with grpc.insecure_channel('order_queue:50051') as order_queue_channel:
        order_queue_stub=order_queue_grpc.OrderQueueServiceStub(order_queue_channel)
        svc = OrderExecutorService(executor_id,know_ids, order_queue_stub)
        svc.start_leader_election()
        svc.run()

def get_all_container_list():
    containers = client.containers.list()
    for i in containers:
        print(i.name, i)
if __name__ == '__main__':
    client = docker.from_env()
    get_all_container_list()
    print(os.getenv("HOSTNAME"))  # Default to "order_executor.0" for testing
    launch_executor("",3)
    """
    replica_id = int(hostname.split('.')[-1])  # Extract the replica number
    print(sys.argv)
    replica_id = int(sys.argv[2])  # Pass replica ID as an argument
    total_replicas = int(sys.argv[3])  # Pass total replicas as an argument
    launch_executor(replica_id, total_replicas)"""