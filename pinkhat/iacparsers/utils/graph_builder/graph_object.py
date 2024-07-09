from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GraphObject:
    name: str
    link: str
    children: list[GraphObject]
    parent: list[GraphObject]
    object: dict

    # def __init__(self, children: GraphObject, parent: GraphObject, object: dict):
    #     self.children = children
    #     self.parent = parent
