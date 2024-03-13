import os

from iacparsers.terraform_core import TerraformCore

test_results = [
    {
        "category": "Terraform AWS",
        "cwe": "CWE-311",
        "file_path": "aws_elasticache_cluster.tf",
        "line_of_code": 1,
        "description": "Resource aws_elasticache_cluster name: transit_enabled doesn't enable encryption",
        "module": "aws_elasticache_cluster",
        "severity": "High",
        "vulnerability_type": "Encrypt Sensitive Data at Rest",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-311",
        "file_path": "aws_elasticache_cluster.tf",
        "line_of_code": 11,
        "description": "Resource aws_elasticache_cluster name: no_encryption_in_transit doesn't enable encryption",
        "module": "aws_elasticache_cluster",
        "severity": "High",
        "vulnerability_type": "Encrypt Sensitive Data at Transit",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-311",
        "file_path": "aws_elasticache_cluster.tf",
        "line_of_code": 11,
        "description": "Resource aws_elasticache_cluster name: no_encryption_in_transit doesn't enable encryption",
        "module": "aws_elasticache_cluster",
        "severity": "High",
        "vulnerability_type": "Encrypt Sensitive Data at Rest",
    },
]


def test_resource_aws_elasticache_cluster():
    test_file_name = "aws_elasticache_cluster.tf"
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
