# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fraud_detection.proto
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
    'fraud_detection.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66raud_detection.proto\x12\x05\x66raud\x1a\x0c\x63ommon.proto\"2\n\rOrderResponse\x12\x10\n\x08is_fraud\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\xea\x01\n\x0c\x46raudService\x12\x31\n\x08SayFraud\x12\x0f.common.Request\x1a\x14.fraud.OrderResponse\x12=\n\x10InitVerification\x12\x1a.common.InitAllInfoRequest\x1a\r.common.Empty\x12\x32\n\rCheckUserData\x12\x0f.common.Request\x1a\x10.common.Response\x12\x34\n\x0f\x43heckCreditCard\x12\x0f.common.Request\x1a\x10.common.Responseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fraud_detection_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ORDERRESPONSE']._serialized_start=46
  _globals['_ORDERRESPONSE']._serialized_end=96
  _globals['_FRAUDSERVICE']._serialized_start=99
  _globals['_FRAUDSERVICE']._serialized_end=333
# @@protoc_insertion_point(module_scope)
