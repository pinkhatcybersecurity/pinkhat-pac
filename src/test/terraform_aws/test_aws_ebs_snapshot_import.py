import os.path

from iacparsers.terraform_aws.ebs.terraform_aws_ebs_snapshot_import import (
    TFAwsEbsSnapshotImport,
)
from iacparsers.terraform_core import TerraformCore


def test_resource_aws_ebs_snapshot_import():
    test_file_name = "aws_ebs_snapshot_import.tf"
    test_file_path = os.path.join("test", "terraform_aws", "test_files", test_file_name)
    with open(test_file_path) as f:
        results = TerraformCore.run_scan(file_name=test_file_name, content=f.read())
        assert 2 == len(results)
        for vulnerability in results:
            assert vulnerability.module == TFAwsEbsSnapshotImport.MODULE_NAME
            assert vulnerability.file_path == test_file_name
            assert vulnerability.cwe == "CWE-311"
            assert vulnerability.category == "Terraform AWS"
            assert vulnerability.severity == "High"
            assert vulnerability.description in [
                (
                    f"Resource {TFAwsEbsSnapshotImport.MODULE_NAME} name: vulnerable"
                    " doesn't enable encryption"
                ),
                (
                    f"Resource {TFAwsEbsSnapshotImport.MODULE_NAME} name: vulnerable_false"
                    " doesn't enable encryption"
                ),
            ]
            assert vulnerability.line_of_code in [18, 34]
            assert vulnerability.vulnerability_type == "Encrypt Sensitive Data at Rest"
