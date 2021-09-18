from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class SwaggerInfo(BaseModel):
    title: str
    description: Optional[str]
    version: str


class SwaggerMethod(BaseModel):
    responses: Dict[str, Dict[str, str]]
    summary: str
    description: Optional[str]
    parameters: Optional[List[Dict]]


class SwaggerPath(BaseModel):
    path: str
    method: SwaggerMethod


class SwaggerDefinition(BaseModel):
    type: str
    properties: Dict
    additional_properties: bool = Field(..., alias="additionalProperties")
    required: List[str]
    description: Optional[str]


class Swagger2Model(BaseModel):
    swagger: str = "2.0"
    info: SwaggerInfo
    host: str  # aka BASE_URL like https://api.example.com
    base_path: str = Field(..., alias="basePath")  # like /api/v3
    schemes: List[str] = ["https"]
    produces: List[str]
    consumes: List[str]
    paths: Dict[str, Dict[str, SwaggerPath]]
    definitions: Dict[str, SwaggerDefinition]
