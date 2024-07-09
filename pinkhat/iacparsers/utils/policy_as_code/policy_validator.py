from typing import Iterator

from loguru import logger

from pinkhat.iacparsers.issue_definition import IssueDefinition
from pinkhat.iacparsers.utils.graph_builder.graph_core import GraphCore
from pinkhat.iacparsers.utils.graph_builder.graph_object import GraphObject
from pinkhat.iacparsers.utils.policy_as_code.policy_as_code_rule_loader import TFRuleLoader
from pinkhat.iacparsers.utils.policy_as_code.policy_data import PolicyData
from pinkhat.iacparsers.utils.template_engine.template_engine import TemplateEngine


class PolicyValidator(TemplateEngine):
    def __init__(self, graph_core: GraphCore, rules: TFRuleLoader, child):
        super().__init__()
        self._graph_core = graph_core
        self._rules = rules
        self._child = child

    def check_policies(self, category: str) -> Iterator[IssueDefinition]:
        for graph_name, graph_object in self._graph_core.get_objects().items():
            for issue_check in self._rules.get_rule_for_module(
                category=category, link=graph_object.link
            ):
                logger.info(
                    f"Checking policy {issue_check.policy.module} for {graph_name}"
                )
                helper_data = None
                if issue_check.rule.helper:
                    helper_data = self.run_helper(
                        helper_template=issue_check.rule.helper,
                        this=graph_object,
                    )
                if helper_data and type(helper_data) is list:
                    for helper in helper_data:
                        yield from self._run_check(
                            graph_name=graph_name,
                            graph_object=graph_object,
                            issue_check=issue_check,
                            helper=helper
                        )
                else:
                    yield from self._run_check(
                        graph_name=graph_name,
                        graph_object=graph_object,
                        issue_check=issue_check,
                        helper=helper_data,
                    )

    def _run_check(
        self,
        graph_name: str,
        graph_object: GraphObject,
        issue_check: PolicyData,
        helper: dict = None,
    ) -> Iterator[IssueDefinition]:
        """
        The method triggers a policy check for a specific graph object.
        """
        try:
            if not (
                self.check_condition(
                    statement=issue_check.rule.statement,
                    this=graph_object,
                    helper=helper,
                )
                is issue_check.rule.report_on
            ):
                return
            failure_message = self.generate_failed_message(
                failed_message_template=issue_check.rule.failureMessage,
                this=graph_object,
            )
        except RuntimeError as runtime_error:
            failure_message = str(runtime_error)
        yield IssueDefinition(
            file_path=str(self._child),
            category=issue_check.policy.category,
            rule_name=issue_check.rule.name,
            module=issue_check.policy.module,
            graph_name=helper.get('graph_name') if helper and type(helper) is dict else graph_name,
            description=issue_check.rule.description,
            remediation=issue_check.rule.remediation,
            issue=failure_message,
            line_of_code=self._get_start_line(graph_object=graph_object, helper=helper)
        )

    @staticmethod
    def _get_start_line(graph_object, helper: dict) -> int | None:
        if helper and type(helper):
            return helper.get("__start_line__")
        if type(graph_object.object) is dict:
            return graph_object.object.get("__start_line__")
