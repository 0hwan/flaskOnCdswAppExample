from flask import Blueprint
from flask_apispec import doc, marshal_with, use_kwargs


from main.models.api_key import ApiKey
from main.models.common.error import (
    ResponseError,
    ERROR_API_KEY_NOT_FOUND,
    SUCCESS_CREATE_BOARD,
    SUCCESS_DELETE_BOARD,
    SUCCESS_PERMANENTLY_DELETE_BOARD,
    SUCCESS_UPDATE_BOARD
)
from main.schema.board import (
    RequestBoardList,
    RequestCreateBoard,
    RequestUpdateBoard,
    ResponseBoardInfo,
    ResponseBoardList
)
