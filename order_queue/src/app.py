"""
Order Queue Service

Defines a priority queue to manage orders with two operations:
Enqueue - Called by Orchestrator to add a new order.
Deque -  Called by Order Executor to process an order. Orders with more items in total have a higher priority. 

"""
import queue
import common_pb2 as common
from concurrent import futures
import grpc
import order_queue_pb2_grpc as order_queue_grpc
from opentelemetry.metrics import Observation

from tracing import get_tracer_and_meter

tracer, meter = get_tracer_and_meter('order_queue')

orders_queued = meter.create_up_down_counter('orders_queued', description='number of orders currently queued in order queue')
orders_accepted = meter.create_counter('orders_accepted', description='number of orders accepted by order queue')
books_ordered = meter.create_counter('books_ordered', description='number of books ordered based on orders accepted by order queue')

class RequestWithPriority:
    def __init__(self, request):
        self.request = request
        self.priority = -sum([item.quantity for item in request.items]) #Negative so more product is prioritized
    def __lt__(self, other):
        return self.priority < other.priority

# Create a class to define the server functions, derived from
# order_queue_pb2_grpc.OrderQueueServiceServicer
class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    def __init__(self):
        self._queue = queue.PriorityQueue()
        meter.create_observable_gauge(
            'orders_in_queue',
            description='Current number of orders in the queue',
            callbacks=[lambda _: [Observation(self._queue.qsize(), {})]]
        )
        # New metrics
        self.failed_dequeues = meter.create_counter(
            'failed_dequeues',
            description='Number of failed dequeue attempts due to empty queue'
        )
        self.max_queue_size = meter.create_up_down_counter(
            'max_queue_size',
            description='Maximum observed queue size during runtime'
        )
        self._max_size = 0
    
    def Enqueue(self, request, context):
        self._queue.put(RequestWithPriority(request))
        orders_queued.add(1)
        orders_accepted.add(1)
        books_ordered.add(sum([item.quantity for item in request.items]))
        # Track max queue size
        current_size = self._queue.qsize()
        if current_size > self._max_size:
            self.max_queue_size.add(current_size - self._max_size)
            self._max_size = current_size
        return common.Empty()
    
    def Dequeue(self, request, context):
        try:
            request = self._queue.get(timeout=2).request
            orders_queued.add(-1)
            return request
        except queue.Empty:
            self.failed_dequeues.add(1)
            context.abort(grpc.StatusCode.ABORTED, 'Queue empty')

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