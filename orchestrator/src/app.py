import random
import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
fraud_detection_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, fraud_detection_grpc_path)
suggestions_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, suggestions_grpc_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc

def check_fraud(request_data) -> fraud_detection.OrderResponse:
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.FraudServiceStub(channel)
        # Call the service through the stub object.
        request = fraud_detection.OrderRequest(items=request_data.get('items', []))
        response = stub.SayFraud(request)
    return response

def get_verification(request_data) -> ...:
    ...

def get_suggestion(request_data) -> suggestions.OrderResponse:
    with grpc.insecure_channel('suggestions:50051') as channel:
        # Create a stub object.
        stub = suggestions_grpc.SuggestionServiceStub(channel)
        # Call the service through the stub object.
        request = suggestions.OrderRequest(items=request_data.get('items', []))
        response = stub.SaySuggest(request)
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

# Define a GET endpoint.
@app.route('/', methods=['GET'])
def index():
    """
    Responds with 'Hello, [name]' when a GET request is made to '/' endpoint.
    """
    # Test the fraud-detection gRPC service.
    response = check_fraud({
        'items': [
            {'name': 'Tere List', 'quantity': 543}
        ]
    })
    # Return the response.
    return response

def FraudVerificationSuggestions(request_data):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        fraud_future = executor.submit(check_fraud, request_data)
        verification_future = executor.submit(get_verification, request_data)
        suggestion_future = executor.submit(get_suggestion, request_data)
        fraud_result = fraud_future.result()
        verification_result = verification_future.result()
        suggestions_result = suggestion_future.result()

    order_id = str(random.randrange(0, 1_000_000_000))

    if fraud_result.is_fraud:
        return {
            'orderId': order_id,
            'status': 'Order Rejected',
            'suggestedBooks': [],
        }
    
    return {
        'orderId': order_id,
        'status': 'Order Accepted',
        'suggestedBooks': [...],
    }

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Get request object data to json
    request_data = json.loads(request.data)
    # Print request object data
    #print("Request Data:", request_data.get('items'))
    print(FraudVerificationSuggestions(request_data))
    #check_fraud_response = check_fraud(request_data)
    #print("Fraud Response:", check_fraud_response)

    # Dummy response following the provided YAML specification for the bookstore
    order_status_response = {
        'orderId': '12345',
        'status': 'Order Approved',
        'suggestedBooks': [
            {'bookId': '123', 'title': 'The Best Book', 'author': 'Author 1'},
            {'bookId': '456', 'title': 'The Second Best Book', 'author': 'Author 2'}
        ]
    }

    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
