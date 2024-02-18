import os

from iacparsers.terraform_core import TerraformCore

test_results = [
    {
        "category": "Terraform AWS",
        "cwe": "CWE-311",
        "file_path": "aws_dynamodb_table.tf",
        "line_of_code": 8,
        "location": "Resource aws_dynamodb_table name: dynamodb_vulnerable"
        " doesn't enable encryption for Dynamo table payment",
        "module": "aws_dynamodb_table",
        "severity": "High",
        "vulnerability_type": "Encrypt Sensitive Data at Rest",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-281",
        "file_path": "aws_dynamodb_table.tf",
        "line_of_code": 1,
        "location": "Resource aws_dynamodb_table name: dynamodb_vulnerable"
        " doesn't enable deletion protection for Dynamo table payment",
        "module": "aws_dynamodb_table",
        "severity": "High",
        "vulnerability_type": "",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-311",
        "file_path": "aws_dynamodb_table.tf",
        "line_of_code": 26,
        "location": "Resource aws_dynamodb_table name: dynamodb_vulnerable_without_server_side_encryption"
        " doesn't enable encryption for Dynamo table users",
        "module": "aws_dynamodb_table",
        "severity": "High",
        "vulnerability_type": "Encrypt Sensitive Data at Rest",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-281",
        "file_path": "aws_dynamodb_table.tf",
        "line_of_code": 26,
        "location": "Resource aws_dynamodb_table name: dynamodb_vulnerable_without_server_side_encryption"
        " doesn't enable deletion protection for Dynamo table users",
        "module": "aws_dynamodb_table",
        "severity": "High",
        "vulnerability_type": "",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-281",
        "file_path": "aws_dynamodb_table.tf",
        "line_of_code": 47,
        "location": "Resource aws_dynamodb_table name: dynamodb_vulnerable_with_server_side_encryption"
        " doesn't enable deletion protection for Dynamo table books",
        "module": "aws_dynamodb_table",
        "severity": "High",
        "vulnerability_type": "",
    },
]


def test_resource_aws_dynamodb_table():
    test_file_name = "aws_dynamodb_table.tf"
    test_file_path = os.path.join("test", "terraform_aws", "test_files", test_file_name)
    with open(test_file_path) as f:
        results = TerraformCore.run_scan(file_name=test_file_name, content=f.read())
        assert len(results) == 5
        for index in range(0, len(results)):
            assert results[index].cwe == test_results[index]["cwe"]
            assert results[index].category == test_results[index]["category"]
            assert results[index].file_path == test_results[index]["file_path"]
            assert results[index].line_of_code == test_results[index]["line_of_code"]
            assert results[index].location == test_results[index]["location"]
            assert results[index].module == test_results[index]["module"]
            assert results[index].severity == test_results[index]["severity"]
            assert (
                results[index].vulnerability_type
                == test_results[index]["vulnerability_type"]
            )
