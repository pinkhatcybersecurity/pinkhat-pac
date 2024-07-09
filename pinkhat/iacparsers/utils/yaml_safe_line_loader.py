from yaml import ScalarNode
from yaml.loader import SafeLoader
from yaml.resolver import BaseResolver


class SafeLineLoader(SafeLoader):
    def __init__(self, stream):
        super().__init__(stream)

    def compose_node(self, parent, index):
        # the line number where the previous token has ended (plus empty lines)
        node = super().compose_node(parent, index)
        node.__start_line__ = self.line + 1
        return node

    def construct_mapping(self, node, deep=False):
        """
        Adds __start_line__ to yaml nodes i.e.
        __start_line_image: 4
        __start_line_restart: 5
        """
        node.value += [
            (
                ScalarNode(
                    tag=BaseResolver.DEFAULT_SCALAR_TAG,
                    value=f"__start_line__{key_node.value}",
                ),
                ScalarNode(
                    tag=BaseResolver.DEFAULT_SCALAR_TAG, value=key_node.__start_line__
                ),
            )
            for key_node, value_node in node.value
        ]
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        mapping["__start_line__"] = node.start_mark.line
        return mapping

    @classmethod
    def load(cls, stream):
        loader = cls(stream)
        try:
            return loader.get_single_data(), loader.descriptions
        finally:
            loader.dispose()
