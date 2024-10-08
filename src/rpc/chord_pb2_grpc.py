# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import chord_pb2 as chord__pb2

GRPC_GENERATED_VERSION = '1.66.0'
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
        + f' but the generated code in chord_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ChordServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FindSuccessor = channel.unary_unary(
                '/chord.ChordService/FindSuccessor',
                request_serializer=chord__pb2.FindSuccessorRequest.SerializeToString,
                response_deserializer=chord__pb2.NodeInfo.FromString,
                _registered_method=True)
        self.GetPredecessor = channel.unary_unary(
                '/chord.ChordService/GetPredecessor',
                request_serializer=chord__pb2.Empty.SerializeToString,
                response_deserializer=chord__pb2.NodeInfo.FromString,
                _registered_method=True)
        self.Notify = channel.unary_unary(
                '/chord.ChordService/Notify',
                request_serializer=chord__pb2.NodeInfo.SerializeToString,
                response_deserializer=chord__pb2.Empty.FromString,
                _registered_method=True)
        self.StoreResource = channel.unary_unary(
                '/chord.ChordService/StoreResource',
                request_serializer=chord__pb2.StoreRequest.SerializeToString,
                response_deserializer=chord__pb2.Empty.FromString,
                _registered_method=True)
        self.LookupResource = channel.unary_unary(
                '/chord.ChordService/LookupResource',
                request_serializer=chord__pb2.LookupRequest.SerializeToString,
                response_deserializer=chord__pb2.LookupResponse.FromString,
                _registered_method=True)
        self.GetFingerTable = channel.unary_unary(
                '/chord.ChordService/GetFingerTable',
                request_serializer=chord__pb2.Empty.SerializeToString,
                response_deserializer=chord__pb2.FingerTableResponse.FromString,
                _registered_method=True)
        self.UpdateSuccessor = channel.unary_unary(
                '/chord.ChordService/UpdateSuccessor',
                request_serializer=chord__pb2.NodeInfo.SerializeToString,
                response_deserializer=chord__pb2.Empty.FromString,
                _registered_method=True)
        self.UpdatePredecessor = channel.unary_unary(
                '/chord.ChordService/UpdatePredecessor',
                request_serializer=chord__pb2.NodeInfo.SerializeToString,
                response_deserializer=chord__pb2.Empty.FromString,
                _registered_method=True)


class ChordServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def FindSuccessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPredecessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Notify(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StoreResource(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LookupResource(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFingerTable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateSuccessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePredecessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChordServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FindSuccessor': grpc.unary_unary_rpc_method_handler(
                    servicer.FindSuccessor,
                    request_deserializer=chord__pb2.FindSuccessorRequest.FromString,
                    response_serializer=chord__pb2.NodeInfo.SerializeToString,
            ),
            'GetPredecessor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPredecessor,
                    request_deserializer=chord__pb2.Empty.FromString,
                    response_serializer=chord__pb2.NodeInfo.SerializeToString,
            ),
            'Notify': grpc.unary_unary_rpc_method_handler(
                    servicer.Notify,
                    request_deserializer=chord__pb2.NodeInfo.FromString,
                    response_serializer=chord__pb2.Empty.SerializeToString,
            ),
            'StoreResource': grpc.unary_unary_rpc_method_handler(
                    servicer.StoreResource,
                    request_deserializer=chord__pb2.StoreRequest.FromString,
                    response_serializer=chord__pb2.Empty.SerializeToString,
            ),
            'LookupResource': grpc.unary_unary_rpc_method_handler(
                    servicer.LookupResource,
                    request_deserializer=chord__pb2.LookupRequest.FromString,
                    response_serializer=chord__pb2.LookupResponse.SerializeToString,
            ),
            'GetFingerTable': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFingerTable,
                    request_deserializer=chord__pb2.Empty.FromString,
                    response_serializer=chord__pb2.FingerTableResponse.SerializeToString,
            ),
            'UpdateSuccessor': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateSuccessor,
                    request_deserializer=chord__pb2.NodeInfo.FromString,
                    response_serializer=chord__pb2.Empty.SerializeToString,
            ),
            'UpdatePredecessor': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdatePredecessor,
                    request_deserializer=chord__pb2.NodeInfo.FromString,
                    response_serializer=chord__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'chord.ChordService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('chord.ChordService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ChordService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def FindSuccessor(request,
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
            '/chord.ChordService/FindSuccessor',
            chord__pb2.FindSuccessorRequest.SerializeToString,
            chord__pb2.NodeInfo.FromString,
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
    def GetPredecessor(request,
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
            '/chord.ChordService/GetPredecessor',
            chord__pb2.Empty.SerializeToString,
            chord__pb2.NodeInfo.FromString,
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
    def Notify(request,
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
            '/chord.ChordService/Notify',
            chord__pb2.NodeInfo.SerializeToString,
            chord__pb2.Empty.FromString,
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
    def StoreResource(request,
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
            '/chord.ChordService/StoreResource',
            chord__pb2.StoreRequest.SerializeToString,
            chord__pb2.Empty.FromString,
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
    def LookupResource(request,
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
            '/chord.ChordService/LookupResource',
            chord__pb2.LookupRequest.SerializeToString,
            chord__pb2.LookupResponse.FromString,
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
    def GetFingerTable(request,
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
            '/chord.ChordService/GetFingerTable',
            chord__pb2.Empty.SerializeToString,
            chord__pb2.FingerTableResponse.FromString,
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
    def UpdateSuccessor(request,
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
            '/chord.ChordService/UpdateSuccessor',
            chord__pb2.NodeInfo.SerializeToString,
            chord__pb2.Empty.FromString,
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
    def UpdatePredecessor(request,
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
            '/chord.ChordService/UpdatePredecessor',
            chord__pb2.NodeInfo.SerializeToString,
            chord__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
