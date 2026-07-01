from dataclasses import dataclass


@dataclass
class GuardResult:

    allowed: bool

    reason: str = ""

    category: str = ""