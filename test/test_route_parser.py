import unittest
from biggu_routing import RouteParser


class RouterTest(unittest.TestCase):
    def test_parser_route_without_placeholder(self):
        parser = RouteParser()
        route = r"/articles/"
        self.assertEqual(parser.parse(route), [
            ['/articles/'],
        ])

    def test_parser_route_with_placeholder(self):
        parser = RouteParser()
        route = r"/articles/{id:\d+}[/{title}]"
        self.assertEqual(parser.parse(route), [
            ['/articles/', ['id', '\\d+']], 
            ['/articles/', ['id', '\\d+'], '/', ['title', '[^/]+']]
        ])
        