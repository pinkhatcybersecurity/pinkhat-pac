from dataclasses import dataclass

from pinkhat.iacparsers.utils.policy_as_code.pac_schema.pac_module_schema import PacModuleSchema
from pinkhat.iacparsers.utils.policy_as_code.pac_schema.pac_policy_schema import PacPolicySchema
from pinkhat.iacparsers.utils.policy_as_code.pac_schema.pac_rule_schema import PacRuleSchema


@dataclass
class PolicyData:
    main: PacPolicySchema
    policy: PacModuleSchema
    rule: PacRuleSchema
