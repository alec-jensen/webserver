import inspect
import logging

from webserver.enums import HTTPMethod
from webserver.typedefs import AsyncFunction
from webserver.exceptions import MethodNotAllowed


def split_path(path: str):
    new_path = path.split("/")
    for p in new_path:
        if p == "":
            new_path.remove(p)
    return new_path


# TODO: PathVarNode class for better/more efficient path variable handling


class RouteNode:
    def __init__(
        self, path: str, method: HTTPMethod, handler: AsyncFunction | None = None
    ):
        self.path = path
        self.method = method
        self.handler = handler
        if handler is not None:
            self.handler_args = inspect.getfullargspec(handler).args
            self.handler_signature = inspect.signature(handler)
        self.children = []
        self.path_vars: list[dict] = []

        for part in split_path(path):
            if part.startswith("{") and part.endswith("}"):
                self.path_vars.append(
                    {"name": part[1:-1], "pos": split_path(path).index(part)}
                )

        logging.debug(
            f"Found path variables {self.path_vars} in route {self.method} {self.path}"
        )

        logging.debug(
            f"Registered route {self.method} {self.path} -> {self.handler} with args {self.handler_args}"
        )

    def add_child(self, child):
        for c in self.children:
            c_path = split_path(c.path)
            child_path = split_path(child.path)
            if c_path[0] == child_path[0]:
                logging.debug(f"Adding child {child} to existing child {c}")
                c.add_child(child)
                return

        logging.debug(f"Adding child {child} to {self}")
        self.children.append(child)

    def get_child(self, path: str, method: HTTPMethod):
        for child in self.children:
            child_path = split_path(child.path)
            path_parts = split_path(path)
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

    def add_route(self, path: str, method: HTTPMethod, handler: AsyncFunction):
        for root in self.roots:
            root_path = split_path(root.path)
            path_parts = split_path(path)
            if root_path == path_parts and root.method == method:
                raise ValueError(f"Route {method.value} {path} already exists")

            # make sure route variables create a new root
            path_vars = []
            for part in path_parts:
                if part.startswith("{") and part.endswith("}"):
                    path_vars.append(part)
            if path_vars:
                logging.debug(
                    f"Adding route {method.value} {path} with path variables {path_vars} to new root"
                )
                self.roots.append(RouteNode(path, method, handler))
                return

            if root_path[0] == path_parts[0]:
                logging.debug(
                    f"Adding route {method.value} {path} to existing root {root}"
                )
                root.add_child(RouteNode(path, method, handler))
                return

        logging.debug(f"Adding route {method.value} {path} to new root")
        self.roots.append(RouteNode(path, method, handler))

    def get_route(self, path: str, method: HTTPMethod) -> RouteNode | None:
        method_mismatch = False

        for root in self.roots:
            root_path = split_path(root.path)
            path_parts = split_path(path)
            if root_path == path_parts and root.method == method:
                return root
            elif root_path[0] == path_parts[0]:
                return root.get_child(path, method)

            # Check path variables
            for var in root.path_vars:
                if var["pos"] < len(path_parts):
                    root_path[var["pos"]] = path_parts[var["pos"]]
                    if root_path == path_parts and root.method == method:
                        logging.debug(f"Paths match with path variables: {root_path} == {path_parts}")
                        logging.debug(f"Method matches: {root.method} == {method}")
                        return root
                    elif root.method != method:
                        method_mismatch = True

        if method_mismatch:
            raise MethodNotAllowed(f"Method {method.value} not allowed for path {path}")

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
