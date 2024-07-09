from pinkhat.iacparsers.core_scanning import CoreScanning


def run_test(test_file_path: str, issues: list[dict]):
    core = CoreScanning()
    core.start_scanning(path=test_file_path)
    results = core.get_vulnerabilities_dict()
    assert len(issues) == len(results)
    for index in range(0, len(results)):
        assert results[index]["file_path"] == issues[index]["file_path"]
        assert results[index]["category"] == issues[index]["category"]
        assert results[index]["rule_name"] == issues[index]["rule_name"]
        assert results[index]["module"] == issues[index]["module"]
        assert results[index]["graph_name"] == issues[index]["graph_name"]
        assert results[index]["description"] == issues[index]["description"]
        assert results[index]["remediation"] == issues[index]["remediation"]
        assert results[index]["issue"] == issues[index]["issue"]
        assert results[index]["line_of_code"] == issues[index]["line_of_code"]
