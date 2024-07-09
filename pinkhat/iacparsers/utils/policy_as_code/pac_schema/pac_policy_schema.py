from msgspec import Struct

from pinkhat.iacparsers.utils.policy_as_code.pac_schema.pac_module_schema import PacModuleSchema


class PacPolicySchema(Struct):
    version: float
    policies: list[PacModuleSchema]
