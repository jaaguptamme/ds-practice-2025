"""
Orchestrator Service

Acts as the central coordinator for the system. It receives requests from the frontend, validates
the data, and orchestrates calls to other backend services (fraud detection, transaction verification,
and suggestions). It combines the results and sends a response back to the frontend.

Sends correct orders to Order Queue Service.

"""
import math
import time
import random
import common_pb2 as common
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc
import books_database_pb2 as books_database
import books_database_pb2_grpc as books_database_grpc

import docker
import grpc
from google.protobuf.json_format import MessageToDict

from opentelemetry.instrumentation.threading import ThreadingInstrumentor
from tracing import get_tracer_and_meter, trace

ThreadingInstrumentor().instrument()
tracer, meter = get_tracer_and_meter('orchestrator')

order_sizes = meter.create_histogram(
    'order_sizes',
    description='sizes of orders (total number of books)',
    explicit_bucket_boundaries_advisory=[*range(0, 11, 2), math.inf]
)
request_durations = meter.create_histogram(
    'request_durations',
    description='duration of request against endpoint in milliseconds',
    unit='ms',
    explicit_bucket_boundaries_advisory=[*range(0, 101, 5), math.inf]
)

def check_fraud(order_id) -> fraud_detection.OrderResponse:
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.FraudServiceStub(channel)
        # Call the service through the stub object.
        vector_clock = common.VectorClock(clocks=[0,0,0])
        request = common.Request(order_id=order_id, vector_clock=vector_clock)
        response = stub.SayFraud(request)
    return response

#def get_verification(order_id) -> common.Response:
#    with grpc.insecure_channel('transaction_verification:50051') as channel:
#        # Create a stub object.
#        stub = transaction_verification_grpc.VerificationServiceStub(channel)
#        # Call the service through the stub object.
#        vector_clock = common.VectorClock(clocks=[0,0,0])
#        request = common.Request(order_id=order_id, vector_clock=vector_clock)
#        response = stub.SayVerification(request)
#    return response

def initTransaction(order_id, request_data):
    with grpc.insecure_channel('transaction_verification:50051') as channel:
        # Create a stub object.
        stub = transaction_verification_grpc.VerificationServiceStub(channel)
        # Call the service through the stub object.
        billing_address = request_data['billingAddress']
        billing_address = f"{billing_address['street']}, {billing_address['zip']}, {billing_address['city']}, {billing_address['state']}, {billing_address['country']}"
        request = transaction_verification.TransactionRequest(
            name=request_data['user']['name'],
            contact=request_data['user']['contact'],
            credit_card_number=request_data['creditCard']['number'],
            expiration_date=request_data['creditCard']['expirationDate'],
            cvv=int(request_data['creditCard']['cvv']),
            billing_address=billing_address,
            quantity=sum(item['quantity'] for item in request_data['items']),
            items=request_data.get('items', [])
        )
        request = transaction_verification.InitRequest(order_id=order_id, transaction_request=request)
        response = stub.initVerification(request)
    return response

def initFraudVerification(order_id, request_data):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.FraudServiceStub(channel)
        # Call the service through the stub object.
        request = common.ItemsInitRequest(order_id=order_id, items=request_data.get('items', []))
        response = stub.InitVerification(request)
    return response

def get_suggestion(order_id) -> suggestions.Suggestions:
    with grpc.insecure_channel('suggestions:50051') as channel:
        # Create a stub object.
        stub = suggestions_grpc.SuggestionServiceStub(channel)
        # Call the service through the stub object.
        vector_clock = common.VectorClock(clocks=[0,0,0])
        request = common.Request(order_id=order_id, vector_clock=vector_clock)
        response = stub.SaySuggest(request)
    return response

def init_suggestion(order_id, request_data):
    with grpc.insecure_channel('suggestions:50051') as channel:
        # Create a stub object.
        stub = suggestions_grpc.SuggestionServiceStub(channel)
        # Call the service through the stub object.
        request = common.ItemsInitRequest(order_id=order_id, items=request_data.get('items', []))
        response = stub.initSuggestion(request)
    return response

# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request
from flask_cors import CORS
import json
import threading

# Create a simple Flask app.
app = Flask(__name__)
# Disable sorting of keys in JSON responses
app.json.sort_keys = False
# Enable CORS for the app.
CORS(app, resources={r'/*': {'origins': '*'}})

vectorClocks = dict() #order_id -> vector_clock
def comibine_vector_clock(order_id, new_clock):
    vectorClocks[order_id] = [max(old, new) for old, new in zip(vectorClocks[order_id], new_clock.clocks)]

@tracer.start_as_current_span('a')
def event_a(order_id, transaction_stub: transaction_verification_grpc.VerificationServiceStub,
            fraud_detection_stub: fraud_detection_grpc.FraudServiceStub,
            suggestions_stub: suggestions_grpc.SuggestionServiceStub):
    print("EVENT A START: ",vectorClocks[order_id])
    resp = transaction_stub.BookListNotEmtpy(common.Request(order_id=order_id, vector_clock=common.VectorClock(clocks=vectorClocks[order_id])))
    if resp.fail:
        raise FailException(resp.message)
    comibine_vector_clock(order_id, resp.vector_clock)
    print("VECTOR CLOCK A:",vectorClocks[order_id])
    event_c(order_id, transaction_stub, fraud_detection_stub, suggestions_stub)

@tracer.start_as_current_span('b')
def event_b(order_id, 
            transaction_stub: transaction_verification_grpc.VerificationServiceStub, 
            fraud_detection_stub: fraud_detection_grpc.FraudServiceStub,
            suggestions_stub: suggestions_grpc.SuggestionServiceStub):
    print("EVENT B START: ",vectorClocks[order_id])
    resp = transaction_stub.UserDataVerification(common.Request(order_id=order_id, 
                                                            vector_clock=common.VectorClock(clocks=vectorClocks[order_id])))
    if resp.fail:
        raise FailException(resp.message)
    comibine_vector_clock(order_id, resp.vector_clock)
    print("VECTOR CLOCK B:",vectorClocks[order_id])
    event_d(order_id, fraud_detection_stub,suggestions_stub)

@tracer.start_as_current_span('c')
def event_c(order_id,transaction_stub: transaction_verification_grpc.VerificationServiceStub,
            fraud_detection_stub: fraud_detection_grpc.FraudServiceStub,
            suggestions_stub: suggestions_grpc.SuggestionServiceStub):
    print("EVENT C START: ",vectorClocks[order_id])
    resp = transaction_stub.CreditCardVerification(common.Request(order_id=order_id, 
                                                            vector_clock=common.VectorClock(clocks=vectorClocks[order_id])))    
    if resp.fail:
        raise FailException(resp.message)
    comibine_vector_clock(order_id, resp.vector_clock)
    print("VECTOR CLOCK C:",vectorClocks[order_id])
    event_e(order_id, fraud_detection_stub, suggestions_stub)

@tracer.start_as_current_span('d')
def event_d(order_id, fraud_detection_stub: fraud_detection_grpc.FraudServiceStub,
            suggestions_stub: suggestions_grpc.SuggestionServiceStub):
    print("EVENT D START: ", vectorClocks[order_id])
    resp = fraud_detection_stub.CheckUserData(common.Request(order_id=order_id,vector_clock=common.VectorClock(clocks=vectorClocks[order_id])))
    if resp.fail:
        raise FailException(resp.message)
    print("VECTOR CLOCK D:",vectorClocks[order_id])
    comibine_vector_clock(order_id, resp.vector_clock)
    event_e(order_id, fraud_detection_stub, suggestions_stub)

@tracer.start_as_current_span('e')
def event_e(order_id, 
            fraud_detection_stub: fraud_detection_grpc.FraudServiceStub,
            suggestions_stub: suggestions_grpc.SuggestionServiceStub):
    #fraud-detection service checks the credit card data for fraud.
    print("EVENT E START: ", vectorClocks[order_id])
    resp = fraud_detection_stub.CheckCreditCard(common.Request(order_id=order_id, vector_clock=common.VectorClock(clocks=vectorClocks[order_id])))
    if resp.fail:
        raise FailException(resp.message)
    if resp.message == "Early stop":
        return
    print("VECTOR CLOCK E:",vectorClocks[order_id])
    comibine_vector_clock(order_id, resp.vector_clock)
    event_f(order_id, suggestions_stub)

@tracer.start_as_current_span('f')
def event_f(order_id,
            suggestions_stub: suggestions_grpc.SuggestionServiceStub):
    print("EVENT F START: ", vectorClocks[order_id])
    resp = suggestions_stub.SaySuggest(common.Request(order_id=order_id, vector_clock=common.VectorClock(clocks=vectorClocks[order_id])))
    comibine_vector_clock(order_id, resp.vector_clock)
    print("VECTOR CLOCK F:",vectorClocks[order_id])
    print("F: suggested books: ",resp.books)
    raise BookException(resp.books)

class BookException(Exception):
    pass
class FailException(Exception):
    pass

@tracer.start_as_current_span('checkout')
def FraudVerificationSuggestions(request_data):
    span = trace.get_current_span()
    
    order_id = str(random.randrange(0, 1_000_000_000))
    span.set_attribute('order_id', order_id)

    vectorClocks[order_id] = [0,0,0]
    with grpc.insecure_channel('fraud_detection:50051') as fraud_detection_channel:
        with grpc.insecure_channel('transaction_verification:50051') as transcation_verifiction_channel:
            with grpc.insecure_channel('suggestions:50051') as suggestions_channel:
                #Initing everything
                fraud_detection_stub = fraud_detection_grpc.FraudServiceStub(fraud_detection_channel)
                transaction_verification_stub = transaction_verification_grpc.VerificationServiceStub(transcation_verifiction_channel)
                suggestions_stub = suggestions_grpc.SuggestionServiceStub(suggestions_channel)
                billing_address = request_data['billingAddress']
                general_request  = common.InitAllInfoRequest(order_id=order_id, request=common.AllInfoRequest(
                    name=request_data['user']['name'],
                    contact=request_data['user']['contact'],
                    credit_card_number=request_data['creditCard']['number'],
                    expiration_date=request_data['creditCard']['expirationDate'],
                    cvv=int(request_data['creditCard']['cvv']),
                    billing_address = f"{billing_address['street']}, {billing_address['zip']}, {billing_address['city']}, {billing_address['state']}, {billing_address['country']}",
                    quantity=sum(item['quantity'] for item in request_data['items']),
                    items=request_data.get('items', [])))
                suggestions_request = common.ItemsInitRequest(order_id=order_id, items=request_data.get('items', []))
                fraud_detection_stub.InitVerification(general_request)
                transaction_verification_stub.initVerification(general_request)
                suggestions_stub.initSuggestion(suggestions_request)
                
                suggested_books = None
                fail_error = None

                #Wrapper around threads, that catches returned message
                def thread_wrapper(target, args):
                    try:
                        target(*args)
                    except BookException as e:#Suggestions
                        nonlocal suggested_books                  
                        suggested_books = e.args[0]
                    except FailException as e:#Some kind of an error message
                        nonlocal fail_error
                        fail_error = e
                        
                t_a = threading.Thread(target=thread_wrapper, args=(event_a, (order_id, transaction_verification_stub, fraud_detection_stub, suggestions_stub)))    
                t_b = threading.Thread(target=thread_wrapper, args=(event_b, (order_id, transaction_verification_stub, fraud_detection_stub, suggestions_stub)))
                t_a.start()
                t_b.start()
                t_a.join()
                t_b.join()
                if fail_error is not None:
                    return {
                        'orderId': order_id,
                        'status': f'Order Rejected: {fail_error}',
                        'suggestedBooks': []
                    }
                elif suggested_books is not None:
                    # ALL CORRECT, SO send to order queue
                    with grpc.insecure_channel('order_queue:50051') as order_queue_channel:
                        order_queue_stub = order_queue_grpc.OrderQueueServiceStub(order_queue_channel)
                        items_to_send = common.ItemsInitRequest(order_id=order_id, items=request_data.get('items', []))
                        order_queue_stub.Enqueue(items_to_send)
                    order_sizes.record(general_request.request.quantity)
                    # Finally return books to frontend
                    return {
                        'orderId': order_id,
                        'status': 'Order Approved',
                        'suggestedBooks': [MessageToDict(book) for book in suggested_books], # type: ignore
                    }
                else:
                    raise AssertionError("Unexpected error occurred, threads did not terminate in an expected way")

    return {
            'orderId': order_id,
            'status': 'Order Rejected',
            'suggestedBooks': [],
        }

def get_db_replica_ids():
    client = docker.from_env()
    
    known_ids = ['books_database_primary']
    for container in client.containers.list(all=True):
        if container.labels.get('com.docker.compose.service') == 'books_database':
            known_ids.append(container.short_id)
    
    return known_ids

db_replica_ids = get_db_replica_ids()

def get_inventory(book_title: str):  
    values = {}
    for id in db_replica_ids:
        with grpc.insecure_channel(f'{id}:50051') as channel:
            stub = books_database_grpc.BooksDatabaseStub(channel)
            values[id] = stub.Read(books_database.ReadRequest(title=book_title)).stock

    return values

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    start = time.perf_counter()

    # Get request object data to json
    request_data = json.loads(request.data)
    
    # Make requests to other services and return response
    response = FraudVerificationSuggestions(request_data)

    end = time.perf_counter()
    request_durations.record((end - start) * 1000, {'endpoint': '/checkout'})

    return response

@app.route('/inventory', methods=['GET'])
def inventory():
    """
    Responds with a JSON object containing database value for each replica. For debugging purposes.
    """
    start = time.perf_counter()

    book_title = request.args.get('title')
    
    response = get_inventory(book_title)

    end = time.perf_counter()
    request_durations.record((end - start) * 1000, {'endpoint': '/inventory'})

    return response

if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')