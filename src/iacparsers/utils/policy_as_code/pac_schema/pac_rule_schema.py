from typing import Optional

from msgspec import Struct


class PacRuleSchema(Struct):
    name: str
    link: str
    statement: str
    report_on: Optional[bool] = False
    description: Optional[str] = None
    remediation: Optional[str] = None
    failureMessage: Optional[str] = None
    helper: Optional[str] = None
