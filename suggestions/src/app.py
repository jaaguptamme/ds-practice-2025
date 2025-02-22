import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
suggestions_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, suggestions_grpc_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# suggestions_pb2_grpc.HelloServiceServicer
class SuggestionsService(suggestions_grpc.SuggestionServiceServicer):
    # Create an RPC function to say hello
    def SaySuggest(self, request, context):
        # Create a HelloResponse object
        response = suggestions.SuggestionResponse()
        # Set the greeting field of the response object
        response.message = "Hello, "
        # Print the greeting message
        print(response.message)
        # Return the response object
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    #suggestions_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    suggestions_grpc.add_SuggestionServiceServicer_to_server(SuggestionsService(), server)
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