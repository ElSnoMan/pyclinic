from typing import Any, Dict, List, Optional, Union
from typing import Optional
from pydantic import BaseModel, Field


class PostmanCollectionInfo(BaseModel):
    postman_id: str = Field(..., alias="_postman_id")
    name: str
    postman_schema: str = Field(..., alias="schema")


class PostmanCollectionVariable(BaseModel):
    key: str
    value: str
    type: str


class PostmanRequestQuery(BaseModel):
    key: str
    value: str


class PostmanRequestUrl(BaseModel):
    raw: str
    protocol: Optional[str]
    host: List[str]
    path: List[str]
    query: Optional[List[PostmanRequestQuery]]


class PostmanRequest(BaseModel):
    """If the method is POST, then url is a str"""
    method: str
    header: List[Dict]
    url: Union[PostmanRequestUrl, str]


class PostmanResponse(BaseModel):
    name: str
    original_request: PostmanRequest = Field(..., alias="originalRequest")
    status: str
    code: int
    header: List[Dict]
    cookie: List[Dict]
    body: Any


class PostmanItem(BaseModel):
    name: str
    request: PostmanRequest
    response: List[PostmanResponse]


class PostmanFolder(BaseModel):
    name: str
    item: List[PostmanItem]


class PostmanCollection(BaseModel):
    info: PostmanCollectionInfo
    variable: Optional[List[PostmanCollectionVariable]]
    folders: Optional[List[PostmanFolder]]
    item: Optional[List[PostmanItem]]
