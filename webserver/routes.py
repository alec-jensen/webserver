import inspect
import logging

from webserver.enums import Methods
from webserver.typedefs import AsyncFunction

def _split_path(path: str):
    new_path = path.split("/")
    for p in new_path:
        if p == "":
            new_path.remove(p)
    return new_path

class RouteNode:
    def __init__(self, path: str, method: Methods, handler: AsyncFunction | None = None):
        self.path = path
        self.method = method
        self.handler = handler
        self.handler_args = inspect.getfullargspec(handler).args
        self.children = []

        logging.debug(f"Registered route {self.method} {self.path} -> {self.handler} with args {self.handler_args}")

    def add_child(self, child):
        for c in self.children:
            c_path = _split_path(c.path)
            child_path = _split_path(child.path)
            if c_path[0] == child_path[0]:
                logging.debug(f"Adding child {child} to existing child {c}")
                c.add_child(child)
                return
            
        logging.debug(f"Adding child {child} to {self}")
        self.children.append(child)

    def get_child(self, path: str, method: Methods):
        for child in self.children:
            child_path = _split_path(child.path)
            path_parts = _split_path(path)
            if child_path == path_parts and child.method == method:
                return child
            elif child_path[0] == path_parts[0]:
                return child.get_child(path, method)

    def __str__(self):
        return f"RouteNode({self.path}, {self.method.value})"

    def __repr__(self):
        return self.__str__()


class RouteTree:
    def __init__(self):
        self.roots: list[RouteNode] = []

    def add_route(self, path: str, method: Methods, handler: AsyncFunction):
        for root in self.roots:
            root_path = _split_path(root.path)
            path_parts = _split_path(path)
            if root_path[0] == path_parts[0]:
                logging.debug(f"Adding route {method.value} {path} to existing root {root}")
                root.add_child(RouteNode(path, method, handler))
                return
        
        logging.debug(f"Adding route {method.value} {path} to new root")
        self.roots.append(RouteNode(path, method, handler))

    def get_route(self, path: str, method: Methods)-> RouteNode | None:
        for root in self.roots:
            root_path = _split_path(root.path)
            path_parts = _split_path(path)
            if root_path == path_parts and root.method == method:
                return root
            elif root_path[0] == path_parts[0]:
                return root.get_child(path, method)
        return None

    def __str__(self):
        return f"RouteTree({self.roots})"

    def __repr__(self):
        return self.__str__()
    
    def print_tree(self):
        for root in self.roots:
            self._print_tree(root, 0)

    def _print_tree(self, node, depth):
        print(" " * depth + str(node))
        for child in node.children:
            self._print_tree(child, depth + 1)
