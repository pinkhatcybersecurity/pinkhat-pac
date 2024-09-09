class Column:
    def __init__(self, name: str, column_type: str, primary_key: bool = False):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
