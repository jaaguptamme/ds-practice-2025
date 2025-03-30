import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb'))
sys.path.insert(0, grpc_path)
import common_pb2 as common
import threading
from concurrent import futures
import grpc
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc


# Create a class to define the server functions, derived from
# order_queue_pb2_grpc.OrderQueueServiceServicer
class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    def __init__(self):
        self._lock = threading.Lock()
        self._queue = []
    
    def Enqueue(self, request, context):
        with self._lock:
            self._queue.append(request)
        print("ENQUEUE",request)
        response = order_queue.EnqueueResponse()
        response.failed = False
        response.message ="Success"
        return response
    
    def Dequeue(self, request, context):
        with self._lock:
            if len(self._queue) == 0:
                response = common.ItemsInitRequest()
                response.items = []
                response.order_id = ""
                return response
            else:
                order = self._queue.pop(0)
                return order
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    order_queue_grpc.add_OrderQueueServiceServicer_to_server(OrderQueueService(), server)
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