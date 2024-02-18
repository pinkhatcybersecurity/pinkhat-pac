import os

from iacparsers.terraform_core import TerraformCore

test_results = [
    {
        "category": "Terraform AWS",
        "cwe": "CWE-281",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 1,
        "location": "Resource aws_rds_cluster name: no_cloud_watch doesn't send logs to cloud watch",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Audit Log Management",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-664",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 1,
        "location": "Resource aws_rds_cluster name: no_cloud_watch insufficient data recovery retention period",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Data Recovery",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-281",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 26,
        "location": "Resource aws_rds_cluster name: nothing doesn't enable deletion protection",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Protect Recovery Data",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-311",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 26,
        "location": "Resource aws_rds_cluster name: nothing doesn't enable encryption",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Encrypt Sensitive Data at Rest",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-281",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 26,
        "location": "Resource aws_rds_cluster name: nothing doesn't send logs to cloud watch",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Audit Log Management",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-664",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 26,
        "location": "Resource aws_rds_cluster name: nothing insufficient data recovery retention period",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Data Recovery",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-281",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 42,
        "location": "Resource aws_rds_cluster name: cloud_watch_enabled doesn't enable deletion protection",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Protect Recovery Data",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-311",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 42,
        "location": "Resource aws_rds_cluster name: cloud_watch_enabled doesn't enable encryption",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Encrypt Sensitive Data at Rest",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-281",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 42,
        "location": "Resource aws_rds_cluster name: cloud_watch_enabled doesn't send logs"
        " to cloud watch for ['error', 'general', 'postgresql', 'slowquery']",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Audit Log Management",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-281",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 60,
        "location": "Resource aws_rds_cluster name: cloud_watch_enabled_all doesn't enable deletion protection",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Protect Recovery Data",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-311",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 60,
        "location": "Resource aws_rds_cluster name: cloud_watch_enabled_all doesn't enable encryption",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Encrypt Sensitive Data at Rest",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-664",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 60,
        "location": "Resource aws_rds_cluster name: cloud_watch_enabled_all there is no preferred maintenance window",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Maintenance Window for OS patching",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-281",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 77,
        "location": "Resource aws_rds_cluster name: cloud_watch_enabled_mssql_all doesn't enable deletion protection",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Protect Recovery Data",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-311",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 77,
        "location": "Resource aws_rds_cluster name: cloud_watch_enabled_mssql_all doesn't enable encryption",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Encrypt Sensitive Data at Rest",
    },
    {
        "category": "Terraform AWS",
        "cwe": "CWE-664",
        "file_path": "aws_rds_cluster.tf",
        "line_of_code": 77,
        "location": "Resource aws_rds_cluster name: cloud_watch_enabled_mssql_all there is no preferred maintenance window",
        "module": "aws_rds_cluster",
        "severity": "High",
        "vulnerability_type": "Maintenance Window for OS patching",
    },
]


def test_aws_rds_cluster():
    test_file_name = "aws_rds_cluster.tf"
    test_file_path = os.path.join("test", "terraform_aws", "test_files", test_file_name)
    with open(test_file_path) as f:
        results = TerraformCore.run_scan(file_name=test_file_name, content=f.read())
        assert len(results) == len(test_results)
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
