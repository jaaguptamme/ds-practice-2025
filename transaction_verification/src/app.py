"""
Transaction Verification Service

Verifies user data, billing addresses, and credit card details. It ensures that all mandatory fields
are filled and valid before approving an order. 

Uses vector clocks to maintain consistency across services.

"""
import common_pb2 as common
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures

def verify_credit_card(request: common.AllInfoRequest):
    if len(str(request.cvv))!=3:
        return False
    if len(str(request.credit_card_number))!=16:
        return False
    return True

def verify_billing_address(request: common.AllInfoRequest):
    correct = True
    values = request.billing_address.split(',')
    if len(values)!=5:
        correct=False
    for value in values:
        if len(value.strip())==0:
            correct=False
    return correct

def verify_contact(request: common.AllInfoRequest):
    valid  = request.contact.strip() != ""
    return valid

def verify_name(request: common.AllInfoRequest):
    valid = request.name.strip() !=""
    return valid

# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.VerificationServiceServicer
class VerificationService(transaction_verification_grpc.VerificationServiceServicer):
    def __init__(self,svc_idx=2,total_svcs=3):
        self.svc_idx=svc_idx
        self.total_svcs=total_svcs
        self.orders={}#orderId -> {data}
    def initVerification(self,request:common.InitAllInfoRequest, context=None):
        order_id=request.order_id
        data=request.request
        self.orders[order_id]={"data":data,"vc":[0]*self.total_svcs}
        print("INIT DONE")
        return common.Empty()
    
    def merge_and_incrment(self,local_vc,incoming_vc=0):
        for i in range(self.total_svcs):
            local_vc[i]=max(local_vc[i],incoming_vc[i])
        local_vc[self.svc_idx]+=1

    def BookListNotEmtpy(self, request: common.Request, context) -> common.Response:
        order_id=request.order_id
        incoming_vc=request.vector_clock.clocks
        entry = self.orders.get(order_id)
        data = entry["data"]
        self.merge_and_incrment(entry["vc"],incoming_vc)
        if len(data.items)==0:
            response = common.Response(fail=True, message="Books list is empty", vector_clock=common.VectorClock(clocks=entry["vc"]))
        else: 
            response = common.Response(fail=False, message="", vector_clock=common.VectorClock(clocks=entry["vc"]))
        return response

    def UserDataVerification(self, request, context):
        order_id=request.order_id
        incoming_vc=request.vector_clock.clocks
        entry = self.orders.get(order_id)
        data = entry["data"]
        self.merge_and_incrment(entry["vc"],incoming_vc)
        # Set the greeting field of the response object
        is_correct=True
        message = "All needed data is filled in"
        if verify_contact(data)==False:
            message = "Email should be filled in"
            is_correct=False
        if verify_billing_address(data)==False:
            message = "Billing address should be all filled in"
            is_correct=False
        if verify_name(data)==False:
            message = "Buyer name should be filled in"
            is_correct=False
        response = common.Response(fail= (is_correct==False), message= message, vector_clock=common.VectorClock(clocks=entry["vc"]))
        return response


    def CreditCardVerification(self, request, context):
        order_id=request.order_id
        incoming_vc=request.vector_clock.clocks
        entry = self.orders.get(order_id)
        data = entry["data"]
        self.merge_and_incrment(entry["vc"],incoming_vc)
        # Set the greeting field of the response object
        is_correct=True
        message = "Credit card information is filled in"

        if verify_credit_card(data)==False:
            message = "Credit card information is not in correct format"
            is_correct=False
        
        response = common.Response(fail= (is_correct==False), message= message, vector_clock=common.VectorClock(clocks=entry["vc"]))
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