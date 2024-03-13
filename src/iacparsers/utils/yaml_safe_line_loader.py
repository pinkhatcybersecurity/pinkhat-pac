from yaml.loader import SafeLoader


class SafeLineLoader(SafeLoader):
    def __init__(self, stream):
        super().__init__(stream)

    def compose_node(self, parent, index):
        # the line number where the previous token has ended (plus empty lines)
        node = super().compose_node(parent, index)
        node.__line__ = self.line + 1
        return node

    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        mapping["__line__"] = node.start_mark.line + 1
        return mapping

    @classmethod
    def load(cls, stream):
        loader = cls(stream)
        try:
            return loader.get_single_data(), loader.descriptions
        finally:
            loader.dispose()
