import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb'))
sys.path.insert(0, grpc_path)

import common_pb2 as common
import books_database_pb2 as books_database
import books_database_pb2_grpc as books_database_grpc
from concurrent import futures
import grpc
import docker
import time

class BooksDatabase(books_database_grpc.BooksDatabaseServicer):
    def __init__(self):
        self.store = {}

    def Read(self, request, context):
        stock = self.store.get(request.title, 0)
        return books_database.ReadResponse(stock=stock)
    
    def Write(self, request, context):
        self.store[request.title] = request.new_stock
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