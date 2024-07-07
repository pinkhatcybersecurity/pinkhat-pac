from iacparsers.utils.graph_builder.graph_object import GraphObject


class GraphCore:
    """
    Everything is a some kind of graph i.e. data file structure, EDR diagrams, infrastructure diagrams, family tree etc.
    with parent and children
    - one parent might have multiple children
    - children might be a parent for another children and then becomes a parent
    - in theory it should be easier to find dependencies between different objects
    """

    def __init__(self):
        self._objects = {}

    def add_graph_object(
        self,
        name: str,
        child_name: str | None,
        link: str,
        object_in_graph: dict | object,
    ):
        parent = self._objects.get(
            name, GraphObject(name=name, link=link, children=[], parent=[], object={})
        )
        parent.object = object_in_graph
        parent.link = link
        self._objects[name] = parent
        if child_name:
            self._add_child_to_parent(child_name, parent)

    def _add_child_to_parent(self, child_name: str, parent: GraphObject):
        child: GraphObject = self._objects.get(
            child_name,
            GraphObject(
                name=child_name,
                link="",
                children=[],
                parent=[],
                object={},
            ),
        )
        parent.children.append(child)
        child.parent.append(parent)
        self._objects[child_name] = child

    def get_objects(self) -> dict:
        return self._objects
