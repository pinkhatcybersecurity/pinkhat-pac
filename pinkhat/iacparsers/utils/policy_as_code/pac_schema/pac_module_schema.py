from msgspec import Struct

from pinkhat.iacparsers.utils.policy_as_code.pac_schema.pac_rule_schema import PacRuleSchema


class PacModuleSchema(Struct):
    module: str
    category: str
    rules: list[PacRuleSchema]
