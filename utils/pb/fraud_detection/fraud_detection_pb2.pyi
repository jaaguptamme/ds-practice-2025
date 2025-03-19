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

class InitRequest(_message.Message):
    __slots__ = ("order_id", "order_request")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_REQUEST_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    order_request: OrderRequest
    def __init__(self, order_id: _Optional[str] = ..., order_request: _Optional[_Union[OrderRequest, _Mapping]] = ...) -> None: ...

class FraudRequest(_message.Message):
    __slots__ = ("order_id", "vector_clock")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    vector_clock: VectorClock
    def __init__(self, order_id: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Item(_message.Message):
    __slots__ = ("name", "quantity")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    quantity: int
    def __init__(self, name: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class OrderRequest(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[Item]
    def __init__(self, items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ...) -> None: ...

class OrderResponse(_message.Message):
    __slots__ = ("is_fraud", "message")
    IS_FRAUD_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    is_fraud: bool
    message: str
    def __init__(self, is_fraud: bool = ..., message: _Optional[str] = ...) -> None: ...
