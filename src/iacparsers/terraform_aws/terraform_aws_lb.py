from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TerraformAwsLB:
    """
    Description of *aws_lb* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb

    Class checks aws security checks
    enable_deletion_protection: should be set to True. Default option is False
    """

    MODULE_NAME = "aws_lb"

    @staticmethod
    def security_checks(file_name: str, resource: dict):
        aws_lb = resource.get("aws_lb", [])
        for aws_lb_name in aws_lb:
            resource_aws_lb = aws_lb[aws_lb_name]
            if resource_aws_lb.get("enable_deletion_protection", False) is False:
                VulnerabilityDefinition(
                    file_path=file_name,
                    category="Terraform AWS",
                    vulnerability_type="",
                    severity="High",
                    cwe="CWE-281",
                    module=TerraformAwsLB.MODULE_NAME,
                    vulnerability=f"Resource aws_lb {aws_lb_name} allows to delete AWS Load Balancer at line"
                    f" {resource_aws_lb.get('__start_line__')}",
                )
        # {'resource': [{'aws_lb': {'test': {'name': 'test-lb-tf', 'internal': False, 'load_balancer_type': 'network',
        #                                    'subnets': '${[for subnet in aws_subnet.public : subnet.id]}',
        #                                    'enable_deletion_protection': True, 'tags': {'Environment': 'production'},
        #                                    '__start_line__': 1, '__end_line__': 12}}}]}
