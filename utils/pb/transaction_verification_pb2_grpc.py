# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import common_pb2 as common__pb2
import transaction_verification_pb2 as transaction__verification__pb2

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
        + f' but the generated code in transaction_verification_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class VerificationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SayVerification = channel.unary_unary(
                '/verification.VerificationService/SayVerification',
                request_serializer=common__pb2.Request.SerializeToString,
                response_deserializer=transaction__verification__pb2.TransactionResponse.FromString,
                _registered_method=True)
        self.initVerification = channel.unary_unary(
                '/verification.VerificationService/initVerification',
                request_serializer=transaction__verification__pb2.InitRequest.SerializeToString,
                response_deserializer=common__pb2.Empty.FromString,
                _registered_method=True)
        self.BookListNotEmtpy = channel.unary_unary(
                '/verification.VerificationService/BookListNotEmtpy',
                request_serializer=common__pb2.Request.SerializeToString,
                response_deserializer=common__pb2.Response.FromString,
                _registered_method=True)


class VerificationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SayVerification(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def initVerification(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BookListNotEmtpy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VerificationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SayVerification': grpc.unary_unary_rpc_method_handler(
                    servicer.SayVerification,
                    request_deserializer=common__pb2.Request.FromString,
                    response_serializer=transaction__verification__pb2.TransactionResponse.SerializeToString,
            ),
            'initVerification': grpc.unary_unary_rpc_method_handler(
                    servicer.initVerification,
                    request_deserializer=transaction__verification__pb2.InitRequest.FromString,
                    response_serializer=common__pb2.Empty.SerializeToString,
            ),
            'BookListNotEmtpy': grpc.unary_unary_rpc_method_handler(
                    servicer.BookListNotEmtpy,
                    request_deserializer=common__pb2.Request.FromString,
                    response_serializer=common__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'verification.VerificationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('verification.VerificationService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class VerificationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SayVerification(request,
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
            '/verification.VerificationService/SayVerification',
            common__pb2.Request.SerializeToString,
            transaction__verification__pb2.TransactionResponse.FromString,
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
    def initVerification(request,
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
            '/verification.VerificationService/initVerification',
            transaction__verification__pb2.InitRequest.SerializeToString,
            common__pb2.Empty.FromString,
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
    def BookListNotEmtpy(request,
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
            '/verification.VerificationService/BookListNotEmtpy',
            common__pb2.Request.SerializeToString,
            common__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
