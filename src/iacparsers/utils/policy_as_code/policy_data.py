from dataclasses import dataclass

from iacparsers.utils.policy_as_code.pac_schema.pac_module_schema import PacModuleSchema
from iacparsers.utils.policy_as_code.pac_schema.pac_policy_schema import PacPolicySchema
from iacparsers.utils.policy_as_code.pac_schema.pac_rule_schema import PacRuleSchema


@dataclass
class PolicyData:
    main: PacPolicySchema
    policy: PacModuleSchema
    rule: PacRuleSchema
