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
import grpc
import docker
import time

class BooksDatabase(books_database_grpc.BooksDatabaseServicer):
    def __init__(self):
        self.store = {
            'Book A': 500,
            'Book B': 70,
            'Book C': 10000000,
        }

    def Read(self, request, context):
        stock = self.store.get(request.title, 0)
        return books_database.ReadResponse(stock=stock)
    
    def Write(self, request, context):
        self.store[request.title] = request.new_stock
        return books_database.WriteResponse(success=True)
    
    def DecrementStock(self, request, context):
        stock = self.store.get(request.title, 0)
        if stock<request.amount or request.amount<0:
            return books_database.WriteResponse(success=False)
        self.store[request.title] = stock-request.amount
        return books_database.WriteResponse(success=True)
    
    def IncrementStock(self, request, context):
        stock = self.store.get(request.title, 0)
        if request.amount < 0:
            return books_database.WriteResponse(success=False)
        self.store[request.title] = stock+ request.amount
        return books_database.WriteResponse(success=True)

class PrimaryReplica(BooksDatabase):
    def __init__(self, backup_stubs):
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
        if stock<request.amount or request.amount<0:
            return books_database.WriteResponse(success=False)
        self.store[request.title] = stock-request.amount
        for backup in self.backups:
            try:
                backup.DecrementStock(request)
            except Exception as e:
                print(f"Failed to replicate to backup: {e}")
        return books_database.WriteResponse(success=True)
    
    def IncrementStock(self, request, context):
        stock = self.store.get(request.title, 0)
        if request.amount < 0:
            return books_database.WriteResponse(success=False)
        self.store[request.title] = stock+ request.amount
        for backup in self.backups:
            try:
                backup.IncrementStock(request)
            except Exception as e:
                print(f"Failed to replicate to backup: {e}")
        return books_database.WriteResponse(success=True)
    
class DatabaseParticipant(common_grpc.TransactionService):
    def __init__(self):
        self.temp_updates = {}
    def Prepare(self, request, context):
        self.temp_updates[request.order_id] = request.new_stock 
        return common.PrepareResponse(ready=True)
    def Commit(self, request, context):
        update = self.temp_updates.pop(request.order_id, None)
        if update:
            self.store[request.title] = update
        return common.CommitResponse(success=True)
    def Abort(self, request, context):
        self.temp_updates.pop(request.order_id, None)
        return common.AbortResponse(aborted=True)

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    books_database_grpc.add_BooksDatabaseServicer_to_server(BooksDatabase(), server)
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
