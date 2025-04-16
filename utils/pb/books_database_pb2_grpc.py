# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import books_database_pb2 as books__database__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in books_database_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class BooksDatabaseStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Read = channel.unary_unary(
                '/books_db.BooksDatabase/Read',
                request_serializer=books__database__pb2.ReadRequest.SerializeToString,
                response_deserializer=books__database__pb2.ReadResponse.FromString,
                _registered_method=True)
        self.Write = channel.unary_unary(
                '/books_db.BooksDatabase/Write',
                request_serializer=books__database__pb2.WriteRequest.SerializeToString,
                response_deserializer=books__database__pb2.WriteResponse.FromString,
                _registered_method=True)
        self.DecrementStock = channel.unary_unary(
                '/books_db.BooksDatabase/DecrementStock',
                request_serializer=books__database__pb2.ChangeRequest.SerializeToString,
                response_deserializer=books__database__pb2.WriteResponse.FromString,
                _registered_method=True)
        self.IncrementStock = channel.unary_unary(
                '/books_db.BooksDatabase/IncrementStock',
                request_serializer=books__database__pb2.ChangeRequest.SerializeToString,
                response_deserializer=books__database__pb2.WriteResponse.FromString,
                _registered_method=True)


class BooksDatabaseServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Write(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DecrementStock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IncrementStock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BooksDatabaseServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Read': grpc.unary_unary_rpc_method_handler(
                    servicer.Read,
                    request_deserializer=books__database__pb2.ReadRequest.FromString,
                    response_serializer=books__database__pb2.ReadResponse.SerializeToString,
            ),
            'Write': grpc.unary_unary_rpc_method_handler(
                    servicer.Write,
                    request_deserializer=books__database__pb2.WriteRequest.FromString,
                    response_serializer=books__database__pb2.WriteResponse.SerializeToString,
            ),
            'DecrementStock': grpc.unary_unary_rpc_method_handler(
                    servicer.DecrementStock,
                    request_deserializer=books__database__pb2.ChangeRequest.FromString,
                    response_serializer=books__database__pb2.WriteResponse.SerializeToString,
            ),
            'IncrementStock': grpc.unary_unary_rpc_method_handler(
                    servicer.IncrementStock,
                    request_deserializer=books__database__pb2.ChangeRequest.FromString,
                    response_serializer=books__database__pb2.WriteResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'books_db.BooksDatabase', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('books_db.BooksDatabase', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class BooksDatabase(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Read(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/books_db.BooksDatabase/Read',
            books__database__pb2.ReadRequest.SerializeToString,
            books__database__pb2.ReadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Write(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/books_db.BooksDatabase/Write',
            books__database__pb2.WriteRequest.SerializeToString,
            books__database__pb2.WriteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DecrementStock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/books_db.BooksDatabase/DecrementStock',
            books__database__pb2.ChangeRequest.SerializeToString,
            books__database__pb2.WriteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def IncrementStock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/books_db.BooksDatabase/IncrementStock',
            books__database__pb2.ChangeRequest.SerializeToString,
            books__database__pb2.WriteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
