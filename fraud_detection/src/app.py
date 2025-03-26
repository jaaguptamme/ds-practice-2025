import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb'))
sys.path.insert(0, grpc_path)
import common_pb2 as common
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc
import re
import datetime

import grpc
from concurrent import futures

class FraudService(fraud_detection_grpc.FraudServiceServicer):
    def __init__(self,svc_idx=0,total_svcs=3):
        self.svc_idx=svc_idx
        self.total_svcs=total_svcs
        self.orders={}#orderId -> {data}

    def InitVerification(self,request: common.InitAllInfoRequest, context=None):
        order_id=request.order_id
        data=request.request
        self.orders[order_id]={"data":data,"vc":[0]*self.total_svcs}
        return common.Empty()

    def merge_and_incrment(self,local_vc,incoming_vc=0):
        print(f"local_vc: {local_vc}")
        print(f"incoming_vc: {incoming_vc}")
        for i in range(self.total_svcs):
            local_vc[i]=max(local_vc[i],incoming_vc[i])
        local_vc[self.svc_idx]+=1

    #TODO ACTUALLY IMPLEMENT THIS
    def CheckUserData(self, request: common.Request, context):
        order_id=request.order_id
        incoming_vc=request.vector_clock.clocks
        entry = self.orders.get(order_id)
        data = entry["data"]
        print("AIHDOOAIGHOIEGHEOIHGEOIEGH", entry)
        print("idshogianlanvlkaIhfoiahaoigheoigeauepaiufpajfpanf", data)
        self.merge_and_incrment(entry["vc"],incoming_vc)
        fail = False
        message = ""
        items = data.items
        totalAmount=sum([item.quantity for item in items])
        if(len(items)>=10):
            fail = True
            message = "Ordered too many items"
        elif(totalAmount>=10):
            fail = True
            message = "Ordered too many of the same item"
        #else:
        #    print("CONTAKT", data.contact)
        #    valid  = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data.contact)
        #    if valid == False:
        #        fail = True
        #        message = "Contact should be valid"
            
        response = common.Response(message=message, fail=fail, vector_clock=common.VectorClock(clocks=entry["vc"]))
        return response

    def CheckCreditCard(self, request: common.Request, context):
        order_id=request.order_id
        incoming_vc=request.vector_clock.clocks
        entry = self.orders.get(order_id)
        data = entry["data"]
        self.merge_and_incrment(entry["vc"],incoming_vc)
        print("KINNIII VectorClock=",entry["vc"])
        if (entry["vc"][2] < 3 or entry["vc"][0] < 3):
            response = common.Response(message="Early stop", fail=False, vector_clock=common.VectorClock(clocks=entry["vc"]))
            return response
        #print(data)
        fail=False
        message = "User data is OK"
        #if len(str(request.cvv))!=3:
        #    message = "CVV is wrong"
        #    fail = True
        #if len(str(request.credit_card_number))!=16:
        #    message = "Credit card number is wrong"
        #    fail = True

        #print("KREDIIT KAART")
        #month=int(request.expiration_date.split('/')[0])
        #year=int(request.expiration_date.split('/')[1])
        #current_month = datetime.now().month
        #current_year = (datetime.now().year)%100
        #if current_year>year:
        #    message = "Credit card has expired"
        #    fail = True
        #print("AJAKONTROLLLL")
        #if current_year==year and current_month>month:
        #    message = "Credit card has expired"
        #    fail = True
        response = common.Response(message=message, fail=fail, vector_clock=common.VectorClock(clocks=entry["vc"]))
        return response

    def SayFraud(self, request: common.Request, context):
        print(f"FraudService - Request recieved - {request.vector_clock.clocks}")
        
        order_id=request.order_id
        incoming_vc=request.vector_clock.clocks
        entry = self.orders[order_id]
        data = entry["data"]
        self.merge_and_incrment(entry["vc"],incoming_vc)

        response = fraud_detection.OrderResponse()
        totalAmount=sum([item.quantity for item in data])
        if(len(data)>=10):
            response.is_fraud = True
            response.message = "Ordered too many items"
        elif(totalAmount>=10):
            response.is_fraud = True
            response.message = "Ordered too many of the same item"
        else:
            response.is_fraud = False
            response.message = "Not fraud" 
        print("FraudService - Response: " + response.message)
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    #fraud_detection_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    fraud_detection_grpc.add_FraudServiceServicer_to_server(FraudService(), server)
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