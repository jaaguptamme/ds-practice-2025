# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: suggestions.proto
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
    'suggestions.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11suggestions.proto\x12\x0bsuggestions\"\x1d\n\x0bVectorClock\x12\x0e\n\x06\x63locks\x18\x01 \x03(\r\"\x07\n\x05\x45mpty\"Q\n\x0bInitRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x30\n\rorder_request\x18\x02 \x01(\x0b\x32\x19.suggestions.OrderRequest\"U\n\x11SuggestionRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12.\n\x0cvector_clock\x18\x02 \x01(\x0b\x32\x18.suggestions.VectorClock\"5\n\x04\x42ook\x12\x0e\n\x06\x62ookId\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\"&\n\x04Item\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"0\n\x0cOrderRequest\x12 \n\x05items\x18\x01 \x03(\x0b\x32\x11.suggestions.Item\"/\n\x0bSuggestions\x12 \n\x05\x62ooks\x18\x01 \x03(\x0b\x32\x11.suggestions.Book2\x9b\x01\n\x11SuggestionService\x12\x46\n\nSaySuggest\x12\x1e.suggestions.SuggestionRequest\x1a\x18.suggestions.Suggestions\x12>\n\x0einitSuggestion\x12\x18.suggestions.InitRequest\x1a\x12.suggestions.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'suggestions_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_VECTORCLOCK']._serialized_start=34
  _globals['_VECTORCLOCK']._serialized_end=63
  _globals['_EMPTY']._serialized_start=65
  _globals['_EMPTY']._serialized_end=72
  _globals['_INITREQUEST']._serialized_start=74
  _globals['_INITREQUEST']._serialized_end=155
  _globals['_SUGGESTIONREQUEST']._serialized_start=157
  _globals['_SUGGESTIONREQUEST']._serialized_end=242
  _globals['_BOOK']._serialized_start=244
  _globals['_BOOK']._serialized_end=297
  _globals['_ITEM']._serialized_start=299
  _globals['_ITEM']._serialized_end=337
  _globals['_ORDERREQUEST']._serialized_start=339
  _globals['_ORDERREQUEST']._serialized_end=387
  _globals['_SUGGESTIONS']._serialized_start=389
  _globals['_SUGGESTIONS']._serialized_end=436
  _globals['_SUGGESTIONSERVICE']._serialized_start=439
  _globals['_SUGGESTIONSERVICE']._serialized_end=594
# @@protoc_insertion_point(module_scope)
