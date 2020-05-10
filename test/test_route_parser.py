import unittest
from biggu_routing import RouteParser
from biggu_routing import BadRouteException


class RouterTest(unittest.TestCase):
    def test_parser_for_route_without_placeholder(self):
        parser = RouteParser()
        route = r"/articles/"
        self.assertEqual(parser.parse(route), [
            ['/articles/'],
        ])

    def test_parser_for_route_with_placeholder(self):
        parser = RouteParser()
        route = r"/articles/{id:\d+}[/{title}]"
        self.assertEqual(parser.parse(route), [
            ['/articles/', ['id', '\\d+']], 
            ['/articles/', ['id', '\\d+'], '/', ['title', '[^/]+']]
        ])

    def test_parser_for__basic_route(self):
        parser = RouteParser()
        route = '/test'
        self.assertEqual(parser.parse(route), [
            ['/test'],
        ])  
        
    def test_parser_for_route_with_placeholer_param_as_path_segment(self):
        parser = RouteParser()
        route = '/test/{param}'
        self.assertEqual(parser.parse(route), [
            ['/test/', ['param', '[^/]+']],
        ])
    
    def test_parser_for_route_with_placeholder_in_middle_of_path_segment(self):
        parser = RouteParser()
        route = '/te{ param }st'
        self.assertEqual(parser.parse(route), [
            ['/te', ['param', '[^/]+'], 'st'],
        ])

    def test_parser_for_route_with_multiple_placeholder(self):
        parser = RouteParser()
        route = '/test/{param1}/test2/{param2}'
        self.assertEqual(parser.parse(route), [
            ['/test/', ['param1', '[^/]+'], '/test2/', ['param2', '[^/]+']],
        ])

    def test_parser_for_route_with_regex_params(self):
        parser = RouteParser()
        route = r'/test/{param:\d+}'
        self.assertEqual(parser.parse(route), [
            ['/test/', ['param', r'\d+']],
        ])

    def test_parser_for_route_with_complex_regex_params(self):
        parser = RouteParser()
        route = r'/test/{ param : \d{1,9} }'
        self.assertEqual(parser.parse(route), [
            ['/test/', ['param', r'\d{1,9}']],
        ])
    
    def test_parser_for_route_with_optional_end_path(self):
        parser = RouteParser()
        route = '/test[opt]'
        self.assertEqual(parser.parse(route), [
            ['/test'],
            ['/testopt'],
        ])

    def test_parser_for_route_with_optional_end_path_and_placheholder_inside(self):
        parser = RouteParser()
        route = '/test[/{param}]'
        self.assertEqual(parser.parse(route), [
            ['/test'],
            ['/test/', ['param', '[^/]+']],
        ])   

    def test_parser_for_route_with_placeholder_at_start_and_optional_path_at_end(self):
        parser = RouteParser()
        route = '/test[/{name}[/{id:[0-9]+}]]'
        self.assertEqual(parser.parse(route), [
            ['/test'],
            ['/test/', ['name', '[^/]+']],
            ['/test/', ['name', '[^/]+'], '/', ['id', '[0-9]+']],
        ]) 

    def test_parser_for_route_with_empty_route(self):
        parser = RouteParser()
        route = ''
        self.assertEqual(parser.parse(route), [
            [''],
        ]) 

    def test_parser_for_route_with_single_optional_path(self):
        parser = RouteParser()
        route = '[test]'
        self.assertEqual(parser.parse(route), [
            [''],
            ['test'],
        ])    

    def test_parser_for_route_with_single_placeholder(self):
        parser = RouteParser()
        route = '/{foo-bar}'
        self.assertEqual(parser.parse(route), [
            ['/', ['foo-bar', '[^/]+']],
        ])

    def test_parser_for_route_with_complex_single_placeholder(self):
        parser = RouteParser()
        route = '/{_foo:.*}'
        self.assertEqual(parser.parse(route), [
            ['/', ['_foo', '.*']],
        ])    
    
    def test_parser_raise_exception_for_unclosing_end_optional_path(self): 
        try:
            parser = RouteParser()
            route = '/test[opt'
            parser.parse(route)
        except BadRouteException as error:
            self.assertEqual(error.message, "Number of opening '[' and closing ']' does not match")

    def test_parser_raise_exception_for_unclosing_wrapped_optional_path(self): 
        try:
            parser = RouteParser()
            route = '/test[opt[opt2]'
            parser.parse(route)
        except BadRouteException as error:
            self.assertEqual(error.message, "Number of opening '[' and closing ']' does not match")  

    def test_parser_raise_exception_for_unclosing_start_optional(self): 
        try:
            parser = RouteParser()
            route = '/testopt]'
            parser.parse(route)
        except BadRouteException as error:
            self.assertEqual(error.message, "Number of opening '[' and closing ']' does not match")
    
    def test_parser_raise_exception_for_empty_optional_part(self): 
        try:
            parser = RouteParser()
            route = '/test[]'
            parser.parse(route)
        except BadRouteException as error:
            self.assertEqual(error.message, "Empty optional part") 

    def test_parser_raise_exception_for_optional_part_nested_inside_empty_optional(self): 
        try:
            parser = RouteParser()
            route = '/test[[opt]]'
            parser.parse(route)
        except BadRouteException as error:
            self.assertEqual(error.message, "Empty optional part")   
    
    def test_parser_raise_exception_for_single_optional_part_nested_inside_empty_optional(self): 
        try:
            parser = RouteParser()
            route = '[[test]]'
            parser.parse(route)
        except BadRouteException as error:
            self.assertEqual(error.message, "Empty optional part")

    def test_parser_raise_exception_for_optional_part_at_the_mid_route(self): 
        try:
            parser = RouteParser()
            route = '/test[/opt]/required'
            parser.parse(route)
        except BadRouteException as error:
            self.assertEqual(error.message, "Optional segments can only occur at the end of a route")  