import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb'))
sys.path.insert(0, grpc_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures

class FraudService(fraud_detection_grpc.FraudServiceServicer):
    def __init__(self,svc_idx=0,total_svcs=3):
        self.svc_idx=svc_idx
        self.total_svcs=total_svcs
        self.orders={}#orderId -> {data}

    def InitVerification(self,request: fraud_detection.InitRequest, context=None):
        order_id=request.order_id
        data=request.order_request
        self.orders[order_id]={"data":data,"vc":[0]*self.total_svcs}
        return fraud_detection.Empty()

    def merge_and_incrment(self,local_vc,incoming_vc=0):
        for i in range(self.total_svcs):
            local_vc[i]=max(local_vc[i],incoming_vc[i])
        local_vc[self.svc_idx]+=1

    def SayFraud(self, request: fraud_detection.FraudRequest, context):
        print(f"FraudService - Request recieved - {request.vector_clock.clocks}")
        
        order_id=request.order_id
        incoming_vc=request.vector_clock.clocks
        entry = self.orders[order_id]
        data = entry["data"]
        self.merge_and_incrment(entry["vc"],incoming_vc)

        response = fraud_detection.OrderResponse()
        totalAmount=sum([item.quantity for item in data.items])
        if(len(data.items)>=10):
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