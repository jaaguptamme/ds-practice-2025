from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

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
