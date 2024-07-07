import os

from tests.terraform_aws.core_config import run_test

domain_1024_sha1_issues = [
    {
        "file_path": os.path.join(
            "tests", "certificate", "test_files", "domain_1024_sha1.crt"
        ),
        "category": "certificate",
        "rule_name": "Key Length Requirement",
        "module": "Certificate Validation",
        "graph_name": "PL,Moria,Gondor,Gandalf Ltd,Test,gandalfltd.pl,gandalf@ltd.pl",
        "description": "The used cryptographic key should be strong enough to protect data.\n",
        "remediation": "More information about cryptographic keys can be found in this link "
        "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf\n",
        "issue": "Public key size is: RSA - 1024",
        "line_of_code": None,
    },
    {
        "file_path": os.path.join(
            "tests", "certificate", "test_files", "domain_1024_sha1.crt"
        ),
        "category": "certificate",
        "rule_name": "Use Strong Cryptographic Hashing Algorithms",
        "module": "Certificate Validation",
        "graph_name": "PL,Moria,Gondor,Gandalf Ltd,Test,gandalfltd.pl,gandalf@ltd.pl",
        "description": "Certificates should use SHA-256 for the hashing algorithm, "
        "rather than the older MD5 and SHA-1 algorithms. "
        "These have a number of cryptographic weaknesses, and are not trusted by modern browsers.\n",
        "remediation": "",
        "issue": "Hash algorithm detected sha1WithRSAEncryption",
        "line_of_code": None,
    },
]
domain_2048_1000_days = [
    {
        "file_path": os.path.join(
            "tests", "certificate", "test_files", "domain_2048_1000_days.crt"
        ),
        "category": "certificate",
        "rule_name": "Certificate lifecycle",
        "module": "Certificate Validation",
        "graph_name": "PL,vulnerability,high,big,www.vulnerability.xyz",
        "description": "SSL/TLS certificates cannot be issued for longer than 13 months (397 days)"
        " https://pkic.org/2020/07/09/one-year-certs/\n",
        "remediation": "",
        "issue": "Certificate lifecycle is too long 1000 days",
        "line_of_code": None,
    }
]


def test_certificate_domain_1024_sha1():
    test_file_name = "domain_1024_sha1.crt"
    test_file_path = os.path.join("tests", "certificate", "test_files", test_file_name)
    run_test(test_file_path=test_file_path, issues=domain_1024_sha1_issues)


def test_certificate_domain_2048_1000_days():
    test_file_name = "domain_2048_1000_days.crt"
    test_file_path = os.path.join("tests", "certificate", "test_files", test_file_name)
    run_test(test_file_path=test_file_path, issues=domain_2048_1000_days)


def test_certificate_github():
    test_file_name = "github.crt"
    test_file_path = os.path.join("tests", "certificate", "test_files", test_file_name)
    run_test(test_file_path=test_file_path, issues=[])
