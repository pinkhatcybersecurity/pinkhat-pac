class LinuxFilePermissionValidation:
    @staticmethod
    def validate_permissions(permissions: str) -> bool:
        if permissions[-1:] == "7" or permissions[-2:-1] == "7":
            return True
        return False
