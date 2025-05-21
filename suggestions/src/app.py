"""
Suggestions Service

Provides book suggestions based on users' order. It uses a similarity algorithm
to recommend books that are most relevant to the order.

Uses vector clocks to maintain consistency across services.

"""
import common_pb2 as common
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

def findMostSimilarBooks(order):
    similarBooks = []
    for item in order:
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
    def __init__(self,svc_idx=1,total_svcs=3):
        self.svc_idx=svc_idx
        self.total_svcs=total_svcs
        self.orders={}#orderId -> {data}
    def initSuggestion(self,request, context=None):
        order_id=request.order_id
        data=request.items
        self.orders[order_id]={"data":data,"vc":[0]*self.total_svcs}
        print("INIT DONE")
        return common.Empty()
    def merge_and_incrment(self,local_vc,incoming_vc=0):
        for i in range(self.total_svcs):
            local_vc[i]=max(local_vc[i],incoming_vc[i])
        local_vc[self.svc_idx]+=1
    # Create an RPC function to say hello
    def SaySuggest(self, request, context):
        order_id=request.order_id
        incoming_vc=request.vector_clock.clocks
        print("SuggestionsService - Request received")
        entry = self.orders.get(order_id)
        self.merge_and_incrment(entry["vc"],incoming_vc)
        response = suggestions.Suggestions(vector_clock=common.VectorClock(clocks=entry["vc"]))
        response.books.extend(findMostSimilarBooks(entry["data"]))
        print("SuggestionsService - Response: " + str(response.books))
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