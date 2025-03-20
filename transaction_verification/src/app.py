import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb'))
sys.path.insert(0, grpc_path)
import common_pb2 as common
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
# transaction_verification_pb2_grpc.VerificationServiceServicer
class VerificationService(transaction_verification_grpc.VerificationServiceServicer):
    def __init__(self,svc_idx=0,total_svcs=3):
        self.svc_idx=svc_idx
        self.total_svcs=total_svcs
        self.orders={}#orderId -> {data}
    def initVerification(self,request, context=None):
        order_id=request.order_id
        data=request.transaction_request
        print("HEEEEEEEEEEEEEEEEEEERE")
        self.orders[order_id]={"data":data,"vc":[0]*self.total_svcs}
        return common.Empty()
    def merge_and_incrment(self,local_vc,incoming_vc=0):
        for i in range(self.total_svcs):
            local_vc[i]=max(local_vc[i],incoming_vc[i])
        local_vc[self.svc_idx]+=1
    def SayVerification(self, request, context):
        order_id=request.order_id
        incoming_vc=request.vector_clock.clocks
        entry = self.orders.get(order_id)
        data = entry["data"]
        self.merge_and_incrment(entry["vc"],incoming_vc)
        response = transaction_verification.TransactionResponse()
        # Set the greeting field of the response object
        is_correct=True
        response.message = "Hello, you are get verification"

        if verify_contact(data)==False:
            response.message = "Given contact should be valid email"
            is_correct=False

        if verify_credit_card(data)==False:
            response.message = "Given credit card is not valid"
            is_correct=False
        
        if verify_billing_address(data)==False:
            response.message = "We don't take orders from that country"
            is_correct=False

        response.is_verified=is_correct
        return response
    '''# Create an RPC function to say hello
    def SayVerification(self, request, context):
        print("VerificationService - Request recieved")
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
        print("VerificationService - Response: " + response.message)
        # Return the response object
        return response'''

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