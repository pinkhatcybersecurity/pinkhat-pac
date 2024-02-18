import os.path

from iacparsers.terraform_aws.ebs.terraform_aws_ebs_snapshot_copy import (
    TerraformAwsEbsSnapshotCopy,
)
from iacparsers.terraform_aws.ebs.terraform_aws_ebs_volume import TerraformAwsEbsVolume
from iacparsers.terraform_core import TerraformCore


def test_resource_aws_ebs_snapshot_copy():
    test_file_name = "aws_ebs_snapshot_copy.tf"
    test_file_path = os.path.join("test", "terraform_aws", "test_files", test_file_name)
    with open(test_file_path) as f:
        results = TerraformCore.run_scan(file_name=test_file_name, content=f.read())
        assert 3 == len(results)
        for vulnerability in results:
            assert vulnerability.module in [
                TerraformAwsEbsSnapshotCopy.MODULE_NAME,
                TerraformAwsEbsVolume.MODULE_NAME,
            ]
            assert vulnerability.file_path == test_file_name
            assert vulnerability.cwe == "CWE-311"
            assert vulnerability.category == "Terraform AWS"
            assert vulnerability.severity == "High"
            assert vulnerability.location in [
                (
                    f"Resource {TerraformAwsEbsVolume.MODULE_NAME} name: simple_volume doesn't enable encryption"
                ),
                (
                    f"Resource {TerraformAwsEbsSnapshotCopy.MODULE_NAME} name: vulnerable"
                    " doesn't enable encryption"
                ),
                (
                    f"Resource {TerraformAwsEbsSnapshotCopy.MODULE_NAME} name: vulnerable_false"
                    " doesn't enable encryption"
                ),
            ]
            assert vulnerability.line_of_code in [1, 18, 37]
            assert vulnerability.vulnerability_type == "Encrypt Sensitive Data at Rest"
