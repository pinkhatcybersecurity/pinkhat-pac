import os

from tests.core_config import run_test


issues = [
    {
        "file_path": "tests/docker_compose/test_files_postgresql_compose/postgresql_password.yaml",
        "category": "yaml",
        "rule_name": "PostgreSQL database password in environmental variables",
        "module": "Docker Compose validation",
        "graph_name": "db",
        "description": "Plain text passwords in configuration files might lead to data leakage.\n",
        "remediation": "Consider using docker secrets and passing password via POSTGRES_PASSWORD_FILE "
        " https://hub.docker.com/_/postgres\n",
        "issue": "",
        "line_of_code": 6,
    }
]


def test_docker_compose_postgresql_password():
    test_file_name = "postgresql_password.yaml"
    test_file_path = os.path.join(
        "tests", "docker_compose", "test_files_postgresql_compose", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
