from marshmallow import fields, Schema
from main.schema import RequestPagination, ResponsePagination

class ResponseApiKeyInfo(Schema):
  board_info = fields.Nested(
      BoardInfoSchema,
      requried=True,
      data_key="boardInfo"
  )
