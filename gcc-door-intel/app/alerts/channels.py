"""Pluggable alert channels: console, email (SMTP), generic webhook.

Add a channel by subclassing AlertChannel and registering it in CHANNELS.
Which channels are active is set in config.yaml (alerts.channels). All secrets
(SMTP host/user/password, webhook URL) come from .env — never committed.
"""
from __future__ import annotations

import json
import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from typing import Any

import requests

from ..config import env


class AlertChannel(ABC):
    name: str

    @abstractmethod
    def send(self, subject: str, body: str, payload: dict[str, Any]) -> bool:
        ...


class ConsoleChannel(AlertChannel):
    name = "console"

    def send(self, subject: str, body: str, payload: dict[str, Any]) -> bool:
        print("\n" + "=" * 70)
        print(f"[ALERT] {subject}")
        print("-" * 70)
        print(body)
        print("=" * 70 + "\n")
        return True


class EmailChannel(AlertChannel):
    name = "email"

    def send(self, subject: str, body: str, payload: dict[str, Any]) -> bool:
        host = env("SMTP_HOST")
        sender = env("ALERT_EMAIL_FROM")
        recipients = env("ALERT_EMAIL_TO")
        if not (host and sender and recipients):
            print("[alert:email] SMTP_HOST/ALERT_EMAIL_FROM/ALERT_EMAIL_TO not set; skipping.")
            return False
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipients
        try:
            port = int(env("SMTP_PORT", "587"))
            with smtplib.SMTP(host, port) as server:
                if env("SMTP_USE_TLS", "true").lower() == "true":
                    server.starttls()
                user, pwd = env("SMTP_USER"), env("SMTP_PASSWORD")
                if user and pwd:
                    server.login(user, pwd)
                server.sendmail(sender, [r.strip() for r in recipients.split(",")], msg.as_string())
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"[alert:email] failed: {exc}")
            return False


class WebhookChannel(AlertChannel):
    name = "webhook"

    def send(self, subject: str, body: str, payload: dict[str, Any]) -> bool:
        url = env("ALERT_WEBHOOK_URL")
        if not url:
            print("[alert:webhook] ALERT_WEBHOOK_URL not set; skipping.")
            return False
        try:
            resp = requests.post(
                url,
                json={"text": f"*{subject}*\n{body}", "subject": subject, "data": payload},
                timeout=10,
            )
            resp.raise_for_status()
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"[alert:webhook] failed: {exc}")
            return False


CHANNELS: dict[str, type[AlertChannel]] = {
    ConsoleChannel.name: ConsoleChannel,
    EmailChannel.name: EmailChannel,
    WebhookChannel.name: WebhookChannel,
}
