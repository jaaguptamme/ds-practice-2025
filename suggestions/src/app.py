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

existingBooks=[suggestions.Book(bookId='1',title="The Great Gatsby", author="F. Scott Fitzgerald"),
                suggestions.Book(bookId='2',title="The Catcher in the Rye", author="J.D. Salinger"),
                suggestions.Book(bookId='3',title="To Kill a Mockingbird", author="Harper Lee"),
                suggestions.Book(bookId='4',title="1984", author="George Orwell"),
                suggestions.Book(bookId='5',title="The Lord of the Rings", author="J.R.R. Tolkien"),
                suggestions.Book(bookId='6',title="The Hobbit", author="J.R.R. Tolkien")]

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def findMostSimilarBooks(order: suggestions.OrderRequest):
    similarBooks = []
    for item in order.items:
        mostSimilar=existingBooks[0]
        for book in existingBooks:
            if similar(book.title, item.name) > similar(mostSimilar.title, item.name):
                mostSimilar=book
        if mostSimilar in similarBooks:
            continue
        similarBooks.append(mostSimilar)
    return similarBooks

# Create a class to define the server functions, derived from
# suggestions_pb2_grpc.SuggestionServiceServicer
class SuggestionsService(suggestions_grpc.SuggestionServiceServicer):
    # Create an RPC function to say hello
    def SaySuggest(self, request, context):
        print("Suggestion request received")
        response = suggestions.Suggestions()
        response.books.extend(findMostSimilarBooks(request))
        print("Suggestion response sent")
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