from typing import Any, List
from pydantic import BaseModel, Field


class PostmanVariableValue(BaseModel):
    key: str
    value: Any
    enabled: bool


class PostmanVariables(BaseModel):
    id: str
    name: str
    values: List[PostmanVariableValue]
    variable_scope: str = Field(..., alias="_postman_variable_scope")
    exported_at: str = Field(..., alias="_postman_exported_at")
    exported_using: str = Field(..., alias="_postman_exported_using")
