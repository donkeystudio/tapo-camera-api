from dataclasses import dataclass


@dataclass
class Privacy:
    host: str
    privacy_enabled: bool
    name: str


@dataclass
class PrivacyResponse:
    data: [Privacy]
    status: str = 'OK'
