# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: transaction_verification.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'transaction_verification.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1etransaction_verification.proto\x12\x0cverification\x1a\x0c\x63ommon.proto\"^\n\x0bInitRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12=\n\x13transaction_request\x18\x02 \x01(\x0b\x32 .verification.TransactionRequest\"\xbd\x01\n\x12TransactionRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\x12\x1a\n\x12\x63redit_card_number\x18\x03 \x01(\t\x12\x17\n\x0f\x65xpiration_date\x18\x04 \x01(\t\x12\x0b\n\x03\x63vv\x18\x05 \x01(\x05\x12\x17\n\x0f\x62illing_address\x18\x06 \x01(\t\x12\x10\n\x08quantity\x18\x07 \x01(\x05\x12\x1b\n\x05items\x18\x08 \x03(\x0b\x32\x0c.common.Item\";\n\x13TransactionResponse\x12\x13\n\x0bis_verified\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\xd1\x01\n\x13VerificationService\x12\x45\n\x0fSayVerification\x12\x0f.common.Request\x1a!.verification.TransactionResponse\x12<\n\x10initVerification\x12\x19.verification.InitRequest\x1a\r.common.Empty\x12\x35\n\x10\x42ookListNotEmtpy\x12\x0f.common.Request\x1a\x10.common.Responseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_verification_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_INITREQUEST']._serialized_start=62
  _globals['_INITREQUEST']._serialized_end=156
  _globals['_TRANSACTIONREQUEST']._serialized_start=159
  _globals['_TRANSACTIONREQUEST']._serialized_end=348
  _globals['_TRANSACTIONRESPONSE']._serialized_start=350
  _globals['_TRANSACTIONRESPONSE']._serialized_end=409
  _globals['_VERIFICATIONSERVICE']._serialized_start=412
  _globals['_VERIFICATIONSERVICE']._serialized_end=621
# @@protoc_insertion_point(module_scope)
