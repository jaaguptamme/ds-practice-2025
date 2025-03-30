import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EnqueueResponse(_message.Message):
    __slots__ = ("failed", "message")
    FAILED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    failed: bool
    message: str
    def __init__(self, failed: bool = ..., message: _Optional[str] = ...) -> None: ...
