"""
Payment Service

Handles payment transactions for orders. 

Supports Prepare, Commit, and Abort operations for distributed transactions.
Ensures that payments are either fully processed or rolled back in case of failure.
Provides gRPC endpoints for transaction management.
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

import grpc
from concurrent import futures


class PaymentService(common_grpc.TransactionService):
    def __init__(self):
        self.prepared = False 
    def Prepare(self, request, context):
        self.prepared = True 
        return common.PrepareResponse(ready=True)
    def Commit(self, request, context):
        if self.prepared:
            print("Payment commited for order", request.order_id)
            self.prepared = False 
        return common.CommitResponse(success=True)
    def Abort(self, request, context):
        self.prepared = False 
        print("Payment aborted for", request.order_id)
        return common.AbortResponse(aborted=True)
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    #transaction_verification_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    common_grpc.add_TransactionServiceServicer_to_server(PaymentService(),server)
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