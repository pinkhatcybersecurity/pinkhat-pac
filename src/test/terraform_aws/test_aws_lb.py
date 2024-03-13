import os

from iacparsers.terraform_core import TerraformCore

test_results = [
    {
        "category": "Terraform AWS",
        "cwe": "",
        "file_path": "aws_lb.tf",
        "line_of_code": 1,
        "description": "Resource aws_lb name: test has disabled connection log for application load balancer",
        "module": "aws_lb",
        "severity": "High",
        "vulnerability_type": "Disabled Connection Logs for Application Load Balancer",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-664",
        "description": "Resource aws_lb name: missing_enable_deletion_protection there is no enabled deletion protection",
        "file_path": "aws_lb.tf",
        "line_of_code": 22,
        "module": "aws_lb",
        "severity": "High",
        "vulnerability_type": "Enable Deletion Protection",
    },
    {
        "category": "Terraform AWS",
        "cwe": "",
        "description": "Resource aws_lb name: missing_enable_deletion_protection has disabled connection log for application load balancer",
        "file_path": "aws_lb.tf",
        "line_of_code": 22,
        "module": "aws_lb",
        "severity": "High",
        "vulnerability_type": "Disabled Connection Logs for Application Load Balancer",
    },
]


def test_aws_lb():
    test_file_name = "aws_lb.tf"
    test_file_path = os.path.join("test", "terraform_aws", "test_files", test_file_name)
    with open(test_file_path) as f:
        results = TerraformCore.run_scan(file_name=test_file_name, content=f.read())
        assert len(results) == len(test_results)
        for index in range(0, len(results)):
            assert results[index].cwe == test_results[index]["cwe"]
            assert results[index].category == test_results[index]["category"]
            assert results[index].file_path == test_results[index]["file_path"]
            assert results[index].line_of_code == test_results[index]["line_of_code"]
            assert results[index].description == test_results[index]["description"]
            assert results[index].module == test_results[index]["module"]
            assert results[index].severity == test_results[index]["severity"]
            assert (
                results[index].vulnerability_type
                == test_results[index]["vulnerability_type"]
            )
