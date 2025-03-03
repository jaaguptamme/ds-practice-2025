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
from datetime import datetime
import re

def verify_credit_card(request: transaction_verification.TransactionRequest):
    if len(str(request.cvv))!=3:
        return False
    if len(str(request.credit_card_number))!=16:
        return False
    month=int(request.expiration_date.split('/')[0])
    year=int(request.expiration_date.split('/')[1])
    current_month = datetime.now().month
    current_year = (datetime.now().year)%100
    if current_year>year:
        return False
    if current_year==year and current_month>month:
        return False
    return True

def verify_billing_address(request: transaction_verification.TransactionRequest):
    bad_countries  = ['Russia', 'North Korea', 'Spain', 'Greenland']
    for country in bad_countries:
        if country in request.billing_address:
            return False
    return True

def verify_contact(request: transaction_verification.TransactionRequest):
    valid  = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', request.contact)
    return valid

# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.HelloServiceServicer
class VerificationService(transaction_verification_grpc.VerificationServiceServicer):
    # Create an RPC function to say hello
    def SayVerification(self, request, context):
        # Create a HelloResponse object
        response = transaction_verification.TransactionResponse()
        # Set the greeting field of the response object
        is_correct=True
        response.message = "Hello, you are get verification"

        if verify_contact(request)==False:
            response.message = "Given contact should be valid email"
            is_correct=False

        if verify_credit_card(request)==False:
            response.message = "Given credit card is not valid"
            is_correct=False
        
        if verify_billing_address(request)==False:
            response.message = "We don't take orders from that country"
            is_correct=False

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