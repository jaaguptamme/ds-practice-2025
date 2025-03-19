import common_pb2 as _common_pb2
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
    __slots__ = ("order_id", "transaction_request")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_REQUEST_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    transaction_request: TransactionRequest
    def __init__(self, order_id: _Optional[str] = ..., transaction_request: _Optional[_Union[TransactionRequest, _Mapping]] = ...) -> None: ...

class VerificationRequest(_message.Message):
    __slots__ = ("order_id", "vector_clock")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    vector_clock: VectorClock
    def __init__(self, order_id: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class TransactionRequest(_message.Message):
    __slots__ = ("name", "contact", "credit_card_number", "expiration_date", "cvv", "billing_address", "quantity")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    CREDIT_CARD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    BILLING_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    contact: str
    credit_card_number: str
    expiration_date: str
    cvv: int
    billing_address: str
    quantity: int
    def __init__(self, name: _Optional[str] = ..., contact: _Optional[str] = ..., credit_card_number: _Optional[str] = ..., expiration_date: _Optional[str] = ..., cvv: _Optional[int] = ..., billing_address: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class TransactionResponse(_message.Message):
    __slots__ = ("is_verified", "message")
    IS_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    is_verified: bool
    message: str
    def __init__(self, is_verified: bool = ..., message: _Optional[str] = ...) -> None: ...
