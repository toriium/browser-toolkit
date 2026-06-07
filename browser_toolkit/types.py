from dataclasses import dataclass
from typing import TypedDict, Literal, Optional
from enum import StrEnum


class Cookie(TypedDict):
    name: str
    value: str
    domain: str
    path: str
    expires: float
    httpOnly: bool
    secure: bool
    sameSite: Literal["Lax", "None", "Strict"]
    partitionKey: str | None


class LocalStorage(TypedDict):
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
