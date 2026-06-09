from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel


class Cookie(BaseModel):
    name: str
    value: str
    url: str | None = None
    domain: str | None = None
    path: str | None = None
    expires: float | None = None
    httpOnly: bool | None = None
    secure: bool | None = None
    sameSite: Literal["Lax", "None", "Strict"] | None = None
    partitionKey: str | None | None = None


class LocalStorage(BaseModel):
    key: str
    value: str


class RequestType(StrEnum):
    DOCUMENT = "Document"
    XHR = "XHR"
    IMAGE = "Image"
    SCRIPT = "Script"
    STYLESHEET = "Stylesheet"
    FONT = "Font"
    FETCH = "Fetch"
    OTHER = "Other"


@dataclass
class Redirect:
    url: str


@dataclass
class Request:
    url: str
    request_id: str
    cookies: dict
    headers: dict
    redirect: Redirect = None
    type: RequestType = None
