import hcl2
from loguru import logger

from iacparsers.terraform_aws.dynamodb.terraform_aws_dynamodb_table import (
    TFAwsDynamodbTable,
)
from iacparsers.terraform_aws.ebs.terraform_aws_ebs_encryption_by_default import (
    TFAwsEbsEncryptionByDefault,
)
from iacparsers.terraform_aws.ebs.terraform_aws_ebs_snapshot_copy import (
    TFAwsEbsSnapshotCopy,
)
from iacparsers.terraform_aws.ebs.terraform_aws_ebs_snapshot_import import (
    TFAwsEbsSnapshotImport,
)
from iacparsers.terraform_aws.ebs.terraform_aws_ebs_volume import TerraformAwsEbsVolume
from iacparsers.terraform_aws.elasticache.terraform_aws_elasticache_cluster import (
    TFAwsElastiCacheCluster,
)
from iacparsers.terraform_aws.elasticache.terraform_aws_elasticache_replication_group import (
    TFAwsElastiCacheReplicationGroup,
)
from iacparsers.terraform_aws.elb.terraform_aws_lb import TFAwsLB
from iacparsers.terraform_aws.elb.terraform_aws_lb_listener import TFAwsLBListener
from iacparsers.terraform_aws.rds.terraform_aws_db_instance import (
    TFAwsDBInstance,
)
from iacparsers.terraform_aws.rds.terraform_aws_rds_cluster import (
    TFAwsRdsCluster,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TerraformCore:
    FILE_EXTENSION = [".tf"]
    iac_modules = {
        # EBS Group
        TFAwsEbsEncryptionByDefault.MODULE_NAME: lambda file_name,
                                                        component: TFAwsEbsEncryptionByDefault.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TerraformAwsEbsVolume.MODULE_NAME: lambda file_name, component: TerraformAwsEbsVolume.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TFAwsEbsSnapshotCopy.MODULE_NAME: lambda file_name, component: TFAwsEbsSnapshotCopy.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TFAwsEbsSnapshotImport.MODULE_NAME: lambda file_name,
                                                   component: TFAwsEbsSnapshotImport.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        # DynamoDB
        TFAwsDynamodbTable.MODULE_NAME: lambda file_name, component: TFAwsDynamodbTable.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        # RDS
        TFAwsRdsCluster.MODULE_NAME: lambda file_name, component: TFAwsRdsCluster.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TFAwsDBInstance.MODULE_NAME: lambda file_name, component: TFAwsDBInstance.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        # ElastiCache
        TFAwsElastiCacheCluster.MODULE_NAME: lambda file_name,
                                                    component: TFAwsElastiCacheCluster.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TFAwsElastiCacheReplicationGroup.MODULE_NAME: lambda file_name,
                                                             component: TFAwsElastiCacheReplicationGroup.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        # ELB
        TFAwsLB.MODULE_NAME: lambda file_name, component: TFAwsLB.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TFAwsLBListener.MODULE_NAME: lambda file_name, component: TFAwsLBListener.terraform_resource_parser(
            file_name=file_name, component=component
        ),
    }
    only_iac_modules_names = set(iac_modules.keys())

    @staticmethod
    def run_scan(file_name: str, content: str) -> list[VulnerabilityDefinition]:
        results = []
        file_extension = file_name[file_name.rfind("."):]
        if file_extension not in TerraformCore.FILE_EXTENSION:
            return results
        resources = hcl2.loads(text=content, with_meta=True)
        resource: dict
        for resource in resources.get("resource", []):
            component: dict
            results += TerraformCore._parse_terraform_resource(
                file_name=file_name, resource=resource
            )
        return results

    @staticmethod
    def _parse_terraform_resource(file_name: str, resource: dict):
        results = []
        for module, component in resource.items():
            if module not in TerraformCore.only_iac_modules_names:
                continue
            terraform_resource_parser = TerraformCore.iac_modules.get(module)
            if not terraform_resource_parser:
                logger.critical(f"There is no method for {terraform_resource_parser}")
                continue
            results += terraform_resource_parser(
                file_name=file_name, component=component
            )
        return results
