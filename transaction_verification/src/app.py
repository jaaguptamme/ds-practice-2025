import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
transaction_verification_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, transaction_verification_grpc_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures

def verify_credit_card(request: transaction_verification.TransactionRequest):
    if len(str(request.cvv))!=3:
        return False
    if len(str(request.credit_card_number))!=16:
        return False
    return True

# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.HelloServiceServicer
class VerificationService(transaction_verification_grpc.VerificationServiceServicer):
    # Create an RPC function to say hello
    def SayVerification(self, request, context):
        # Create a HelloResponse object
        response = transaction_verification.TransactionResponse()
        # Set the greeting field of the response object
        is_correct=True
        if verify_credit_card(request)==False:
            is_correct=False
        
        if is_correct:
            response.message = "Hello, you are get verification"
        else:
            response.message = "Lick the pan"

        response.is_verified=is_correct
        # Print the greeting message
        print(response.message)
        # Return the response object
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    #transaction_verification_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    transaction_verification_grpc.add_VerificationServiceServicer_to_server(VerificationService(), server)
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