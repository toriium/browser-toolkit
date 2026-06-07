from typing import TypedDict, Literal, Optional


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