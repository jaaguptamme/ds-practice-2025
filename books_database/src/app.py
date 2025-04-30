"""
Books Database Service

Manages the inventory of books, meaning stock levels for each book. 

Called by order executor and propagates info from master node to other replcase

Supports Prepare, Commit, and Abort operations for distributed transactions.
Ensures consistency between the primary and backup replicas using gRPC communication.

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
import common_pb2_grpc as common_grpc
import books_database_pb2 as books_database
import books_database_pb2_grpc as books_database_grpc
from concurrent import futures
import docker
import grpc

class BooksDatabase(books_database_grpc.BooksDatabaseServicer, common_grpc.TransactionService):
    def __init__(self):
        self.store = {
            'Book A': 500,
            'Book B': 70,
            'Book C': 10000000,
        }
        self.temp_updates = {}

    def Read(self, request, context):
        stock = self.store.get(request.title, 0)
        return books_database.ReadResponse(stock=stock)
    
    def Write(self, request, context):
        self.store[request.title] = request.new_stock
        return books_database.WriteResponse(success=True)
    
    # 2PC

    # TODO: Preparing two decrements simultaneously might allow you to store negative amounts

    def Prepare(self, request, context):
        stock = self.store.get(request.title, 0)
        if stock < request.amount or request.amount < 0:
            return common.PrepareResponse(ready=False)
        self.temp_updates[request.order_id] = request
        return common.PrepareResponse(ready=True)

    def Commit(self, request, context):
        prepared_request = self.temp_updates.pop(request.order_id, None)
        if prepared_request is not None:
            response = self.DecrementStock(prepared_request, context)
            print(f"Database update commited for order {request.order_id}, book {request.title}; new stock: {self.store.get(request.title, None)}")
            return common.CommitResponse(success=response.success)
        else:
            return common.CommitResponse(success=False)

    def Abort(self, request, context):
        self.temp_updates.pop(request.order_id, None)
        return common.AbortResponse(aborted=True)

class PrimaryReplica(BooksDatabase):
    def __init__(self, backup_stubs: list[books_database_grpc.BooksDatabaseStub]):
        super().__init__()
        self.backups = backup_stubs
    
    def Write(self, request, context):
        self.store[request.title] = request.new_stock
        
        for backup in self.backups:
            try:
                backup.Write(request)
            except Exception as e:
                print(f"Failed to replicate to backup: {e}")
        
        return books_database.WriteResponse(success=True)
    
    def DecrementStock(self, request, context):
        stock = self.store.get(request.title, 0)
        if stock < request.amount or request.amount < 0:
            return books_database.WriteResponse(success=False)
        self.store[request.title] = stock - request.amount
        
        for backup in self.backups:
            try:
                backup.Write(books_database.WriteRequest(title=request.title, new_stock=self.store[request.title]))
            except Exception as e:
                print(f"Failed to replicate to backup: {e}")
        
        return books_database.WriteResponse(success=True)
    
    def IncrementStock(self, request, context):
        stock = self.store.get(request.title, 0)
        if request.amount < 0:
            return books_database.WriteResponse(success=False)
        self.store[request.title] = stock + request.amount
        
        for backup in self.backups:
            try:
                backup.Write(books_database.WriteRequest(title=request.title, new_stock=self.store[request.title]))
            except Exception as e:
                print(f"Failed to replicate to backup: {e}")
        
        return books_database.WriteResponse(success=True)

def get_backup_ids():
    client = docker.from_env()
    
    known_ids = []
    for container in client.containers.list(all=True):
        if container.labels.get('com.docker.compose.service') == 'books_database':
            known_ids.append(container.short_id)

    return known_ids

def serve():
    is_primary = os.getenv('IS_PRIMARY', '').upper() == 'TRUE'

    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    
    if is_primary:
        backup_stubs = []
        for backup_id in get_backup_ids():
            channel = grpc.insecure_channel(f'{backup_id}:50051')
            stub = books_database_grpc.BooksDatabaseStub(channel)
            backup_stubs.append(stub)
        service = PrimaryReplica(backup_stubs)
    else:
        service = BooksDatabase()
    
    books_database_grpc.add_BooksDatabaseServicer_to_server(service, server)
    common_grpc.add_TransactionServiceServicer_to_server(service, server)
    
    # Listen on port 50051
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50051.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
