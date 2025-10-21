from typing import Any
from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from email.utils import parsedate_to_datetime
from utils import TZ_WARSAW


class Response(BaseModel):
    status: str
    raw: list[Any] | None = None

    @property
    def ok(self) -> bool:
        return self.status.upper() == "OK"


class SelectResponse(Response):
    message_count: int


class EmailMessageModel(BaseModel):
    subject: str
    sender: list[str] | None = None
    to: list[str] | None = None
    #"Secondary recipients (Carbon Copy)
    cc : list[str] | None = None
    # Hidden secondary recipients (Blind Carbon Copy)
    bcc : list[str] | None = None
    date: datetime | None = None
    body: str | None = None
    
    @field_validator('date', mode='before')
    def parse_email_date(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            parsed_dt = parsedate_to_datetime(value)
            return parsed_dt.astimezone(TZ_WARSAW)
        except Exception as e:
            msg = f"Invalid email date: {value!r}"
            raise ValueError(msg) from e


    
    


class FetchResponse(Response):
    message: EmailMessageModel | None = None
