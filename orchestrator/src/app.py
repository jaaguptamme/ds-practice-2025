import random
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
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc
from google.protobuf.json_format import MessageToDict

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

def get_verification(order_id) -> transaction_verification.TransactionResponse:
    with grpc.insecure_channel('transaction_verification:50051') as channel:
        # Create a stub object.
        stub = transaction_verification_grpc.VerificationServiceStub(channel)
        # Call the service through the stub object.
        vector_clock = common.VectorClock(clocks=[0,0,0])
        request = common.Request(order_id=order_id, vector_clock=vector_clock)
        response = stub.SayVerification(request)
    return response

def initTransaction(order_id, request_data):
    with grpc.insecure_channel('transaction_verification:50051') as channel:
        # Create a stub object.
        stub = transaction_verification_grpc.VerificationServiceStub(channel)
        # Call the service through the stub object.
        billing_address = request_data['billingAddress']
        billing_address = f"{billing_address['street']}, {billing_address['zip']} {billing_address['city']}, {billing_address['state']} {billing_address['country']}"
        request = transaction_verification.TransactionRequest(
            name=request_data['user']['name'],
            contact=request_data['user']['contact'],
            credit_card_number=request_data['creditCard']['number'],
            expiration_date=request_data['creditCard']['expirationDate'],
            cvv=int(request_data['creditCard']['cvv']),
            billing_address=billing_address,
            quantity=sum(item['quantity'] for item in request_data['items']),
        )
        request = transaction_verification.InitRequest(order_id=order_id, transaction_request=request)
        response = stub.initVerification(request)
    
    with grpc.insecure_channel('fraud_detection:50051<') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.FraudServiceStub(channel)
        # Call the service through the stub object.
        request = fraud_detection.OrderRequest(items=request_data.get('items', []))
        request = fraud_detection.InitRequest(order_id=order_id, order_request=request)
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
        request = suggestions.OrderRequest(items=request_data.get('items', []))
        request = suggestions.InitRequest(order_id=order_id, order_request=request)
        response = stub.initSuggestion(request)
    return response

# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request
from flask_cors import CORS
import json
import concurrent.futures

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app, resources={r'/*': {'origins': '*'}})

def FraudVerificationSuggestions(request_data):
    order_id = str(random.randrange(0, 1_000_000_000))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        initTransactionFuture = executor.submit(initTransaction, order_id, request_data)
        initSuggestionFuture = executor.submit(init_suggestion, order_id, request_data)
        initTransactionFuture = initTransactionFuture.result()
        initSuggestionFuture = initSuggestionFuture.result()   

    print("WORKS THROUGH INITIALIZATION")  

    with concurrent.futures.ThreadPoolExecutor() as executor:
        fraud_future = executor.submit(check_fraud, order_id)
        verification_future = executor.submit(get_verification, order_id)
        suggestion_future = executor.submit(get_suggestion, order_id)
        fraud_result = fraud_future.result()
        verification_result = verification_future.result()
        suggestions_result = suggestion_future.result()
    
    if fraud_result.is_fraud:
        return {
            'orderId': order_id,
            'status': f'Order Rejected: {fraud_result.message}',
            'suggestedBooks': [],
        }

    if not verification_result.is_verified:
        return {
            'orderId': order_id,
            'status': f'Order Rejected: {verification_result.message}',
            'suggestedBooks': [],
        }
    
    return {
        'orderId': order_id,
        'status': 'Order Approved',
        'suggestedBooks': [MessageToDict(book) for book in suggestions_result.books],
    }

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Get request object data to json
    request_data = json.loads(request.data)
    
    # Make requests to other services and return response
    return FraudVerificationSuggestions(request_data)


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')

