# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import suggestions_pb2 as suggestions__pb2

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
        + f' but the generated code in suggestions_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class SuggestionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SaySuggest = channel.unary_unary(
                '/suggestions.SuggestionService/SaySuggest',
                request_serializer=suggestions__pb2.SuggestionRequest.SerializeToString,
                response_deserializer=suggestions__pb2.Suggestions.FromString,
                _registered_method=True)
        self.initSuggestion = channel.unary_unary(
                '/suggestions.SuggestionService/initSuggestion',
                request_serializer=suggestions__pb2.InitRequest.SerializeToString,
                response_deserializer=suggestions__pb2.Empty.FromString,
                _registered_method=True)


class SuggestionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SaySuggest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def initSuggestion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SuggestionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SaySuggest': grpc.unary_unary_rpc_method_handler(
                    servicer.SaySuggest,
                    request_deserializer=suggestions__pb2.SuggestionRequest.FromString,
                    response_serializer=suggestions__pb2.Suggestions.SerializeToString,
            ),
            'initSuggestion': grpc.unary_unary_rpc_method_handler(
                    servicer.initSuggestion,
                    request_deserializer=suggestions__pb2.InitRequest.FromString,
                    response_serializer=suggestions__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'suggestions.SuggestionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('suggestions.SuggestionService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class SuggestionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SaySuggest(request,
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
            '/suggestions.SuggestionService/SaySuggest',
            suggestions__pb2.SuggestionRequest.SerializeToString,
            suggestions__pb2.Suggestions.FromString,
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
    def initSuggestion(request,
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
            '/suggestions.SuggestionService/initSuggestion',
            suggestions__pb2.InitRequest.SerializeToString,
            suggestions__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
