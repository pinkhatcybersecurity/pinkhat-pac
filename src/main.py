from iacparsers.core_scanning import CoreScanning


def start(path: str):
    core = CoreScanning()
    core.start_scanning(path=path)
    print(core.get_vulnerabilities_dict())


start("test")
