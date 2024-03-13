import os.path

from iacparsers.terraform_aws.ebs.terraform_aws_ebs_encryption_by_default import (
    TFAwsEbsEncryptionByDefault,
)
from iacparsers.terraform_core import TerraformCore


def test_resource_aws_ebs_encryption_by_default():
    test_file_name = "aws_ebs_encryption_by_default.tf"
    test_file_path = os.path.join("test", "terraform_aws", "test_files", test_file_name)
    with open(test_file_path) as f:
        results = TerraformCore.run_scan(file_name=test_file_name, content=f.read())
        assert 1 == len(results)
        for vulnerability in results:
            assert vulnerability.module == TFAwsEbsEncryptionByDefault.MODULE_NAME
            assert vulnerability.file_path == test_file_name
            assert vulnerability.category == "Terraform AWS"
            assert vulnerability.cwe == "CWE-311"
            assert vulnerability.severity == "High"
            assert vulnerability.description == (
                "Resource aws_ebs_encryption_by_default vulnerable"
                " disables default encryption for EBS"
            )
            assert vulnerability.line_of_code == 1
            assert vulnerability.vulnerability_type == "Encrypt Sensitive Data at Rest"
