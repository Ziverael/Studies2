import email
import imaplib
from emails.model import Response, EmailMessageModel, FetchResponse, SelectResponse
from typing import Any
from zoneinfo import ZoneInfo
from email.utils import parsedate_to_datetime

from email.header import decode_header


def decode_mime_header(value: str) -> str:
    if not value:
        return ""
    parts = decode_header(value)
    decoded = ""
    for part, enc in parts:
        if isinstance(part, bytes):
            decoded += part.decode(enc or "utf-8", errors="ignore")
        else:
            decoded += part
    return decoded

def extract_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="ignore")
    else:
        charset = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(charset, errors="ignore")
    return ""



class GmailIMAP:
    def __init__(self, user: str, password: str, host: str = "imap.gmail.com"):
        self.conn = imaplib.IMAP4_SSL(host)
        self.conn.login(user, password)

    def select(self, mailbox: str = "INBOX") -> SelectResponse:
        status, data = self.conn.select(mailbox)
        message_count = int(data[0]) if data and data[0].isdigit() else 0
        return SelectResponse(status=status, raw=data, message_count=message_count)

    def fetch_message(self, index: int) -> FetchResponse:
        status, data = self.conn.fetch(str(index), "(RFC822)")
        if status != "OK" or not data:
            return FetchResponse(status=status, raw=data)

        for response in data:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject = decode_mime_header(msg.get("subject"))
                sender = decode_mime_header(msg.get("from"))
                to = decode_mime_header(msg.get("to"))
                date = decode_mime_header(msg.get("date"))
                body = extract_body(msg)

                parsed = EmailMessageModel(
                    subject=subject,
                    sender=sender,
                    to=to,
                    date=date,
                    body=body
                )
                return FetchResponse(status=status, raw=data, message=parsed)

        return FetchResponse(status=status, raw=data)
    
    def _extract_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                    return part.get_payload(decode=True).decode(errors="ignore")
        else:
            return msg.get_payload(decode=True).decode(errors="ignore")
        return None

