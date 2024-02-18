import hcl2
from loguru import logger

from iacparsers.terraform_aws.dynamodb.terraform_aws_dynamodb_table import (
    TerraformAwsDynamodbTable,
)
from iacparsers.terraform_aws.ebs.terraform_aws_ebs_encryption_by_default import (
    TerraformAwsEbsEncryptionByDefault,
)
from iacparsers.terraform_aws.ebs.terraform_aws_ebs_snapshot_copy import (
    TerraformAwsEbsSnapshotCopy,
)
from iacparsers.terraform_aws.ebs.terraform_aws_ebs_snapshot_import import (
    TerraformAwsEbsSnapshotImport,
)
from iacparsers.terraform_aws.ebs.terraform_aws_ebs_volume import TerraformAwsEbsVolume
from iacparsers.terraform_aws.elasticache.terraform_aws_elasticache_cluster import (
    TerraformAwsElastiCacheCluster,
)
from iacparsers.terraform_aws.elasticache.terraform_aws_elasticache_replication_group import (
    TerraformAwsElastiCacheReplicationGroup,
)
from iacparsers.terraform_aws.rds.terraform_aws_rds_cluster import (
    TerraformAwsRdsCluster,
)
from iacparsers.terraform_aws.rds.terraform_aws_db_instance import (
    TerraformAwsDBInstance,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TerraformCore:
    FILE_EXTENSION = [".tf"]
    iac_modules = {
        # EBS Group
        TerraformAwsEbsEncryptionByDefault.MODULE_NAME: lambda file_name, component: TerraformAwsEbsEncryptionByDefault.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TerraformAwsEbsVolume.MODULE_NAME: lambda file_name, component: TerraformAwsEbsVolume.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TerraformAwsEbsSnapshotCopy.MODULE_NAME: lambda file_name, component: TerraformAwsEbsSnapshotCopy.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TerraformAwsEbsSnapshotImport.MODULE_NAME: lambda file_name, component: TerraformAwsEbsSnapshotImport.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        # DynamoDB
        TerraformAwsDynamodbTable.MODULE_NAME: lambda file_name, component: TerraformAwsDynamodbTable.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        # RDS
        TerraformAwsRdsCluster.MODULE_NAME: lambda file_name, component: TerraformAwsRdsCluster.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TerraformAwsDBInstance.MODULE_NAME: lambda file_name, component: TerraformAwsDBInstance.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        # ElastiCache
        TerraformAwsElastiCacheCluster.MODULE_NAME: lambda file_name, component: TerraformAwsElastiCacheCluster.terraform_resource_parser(
            file_name=file_name, component=component
        ),
        TerraformAwsElastiCacheReplicationGroup.MODULE_NAME: lambda file_name, component: TerraformAwsElastiCacheReplicationGroup.terraform_resource_parser(
            file_name=file_name, component=component
        ),
    }
    only_iac_modules_names = set(iac_modules.keys())

    @staticmethod
    def run_scan(file_name: str, content: str) -> list[VulnerabilityDefinition]:
        results = []
        file_extension = file_name[file_name.rfind(".") :]
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
