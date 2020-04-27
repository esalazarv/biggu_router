import unittest
from biggu_routing import RouteParser


class RouterTest(unittest.TestCase):
    def test_parser_method(self):
        parser = RouteParser()
        route = r"/articles/{id:\d+}[/{title}]"
        self.assertEqual(parser.parse(route), [
            ['/articles/', ['id', '\\d+']], 
            ['/articles/', ['id', '\\d+'], '/', ['title', '[^/]+']]
        ])
        