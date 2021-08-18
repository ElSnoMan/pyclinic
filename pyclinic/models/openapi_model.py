from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field


class ServerObject(BaseModel):
    url: str
    description: Optional[str]
    variables: Optional[Dict[str, Any]]


class ParameterObject(BaseModel):
    name: str
    in_: str = Field(..., alias="in")
    description: str
    required: bool
    deprecated: bool
    allow_empty_value: bool = Field(..., alias="allowEmptyValue")


class ReferenceObject(BaseModel):
    ref: Optional[str] = Field(..., alias="$ref")
    summary: Optional[str]
    description: Optional[str]


class RequestBodyObject(BaseModel):
    description: str
    required: bool
    content: Dict[str, Any]


class OperationObject(BaseModel):
    tags: List[str]
    summary: str
    description: str
    external_docs: Any = Field(..., alias="externalDocs")
    operation_id: str = Field(..., alias="operationId")
    parameters: List[Union[ParameterObject, ReferenceObject]]
    request_body: Union[RequestBodyObject, ReferenceObject] = Field(..., alias="requestBody")
    responses: Dict
    callbacks: Dict[str, Any]
    deprecated: bool
    security: List[Any]
    servers: List[ServerObject]


class PathItemObject(BaseModel):
    ref: str = Field(..., title="$ref")
    summary: str
    description: str
    get: OperationObject
    put: OperationObject
    post: OperationObject
    delete: OperationObject
    options: OperationObject
    head: OperationObject
    patch: OperationObject
    trace: OperationObject
    servers: List[ServerObject]
    parameters: List[ParameterObject]


class InfoObject(BaseModel):
    title: str
    summary: Optional[str]
    description: Optional[str]
    terms_of_service: Optional[str] = Field(..., alias="termsOfService")
    contact: Any
    license: Any
    version: str


class OpenApiModel(BaseModel):
    openapi: str
    info: InfoObject
    json_schema_dialect: Optional[str] = Field(..., alias="jsonSchemaDialect")
    servers: List[ServerObject]
    paths: Dict[str, PathItemObject]
    webhooks: Optional[Dict[str, Any]]
    components: Dict[str, Any]
    security: Optional[List[Any]]
    tags: Optional[List[Any]]
    externalDocs: Optional[Any]
