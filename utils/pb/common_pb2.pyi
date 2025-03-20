from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VectorClock(_message.Message):
    __slots__ = ("clocks",)
    CLOCKS_FIELD_NUMBER: _ClassVar[int]
    clocks: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, clocks: _Optional[_Iterable[int]] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ("order_id", "vector_clock")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    vector_clock: VectorClock
    def __init__(self, order_id: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("fail", "vector_clock")
    FAIL_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    fail: bool
    vector_clock: VectorClock
    def __init__(self, fail: bool = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
