import unittest
from biggu_container import Container
from biggu_router import Router


class RouterTest(unittest.TestCase):
    def test_add_route(self):
        container = Container()
        router = Router(container)
        router.add_route('GET', '/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['GET/home'], {'method': 'GET', 'uri': '/home', 'action': 'test@test'})

    def test_add_route_trim_slashes(self):
        container = Container()
        router = Router(container)
        router.add_route('GET', '/home/', {'as': 'home', 'uses': 'test@test'})
        routes = router.named_routes
        self.assertEqual(routes['home'], '/home')

    def test_add_route_with_alias(self):
        container = Container()
        router = Router(container)
        router.add_route('GET', '/home', {'as': 'home', 'uses': 'test@test'})
        routes = router.named_routes
        self.assertEqual(routes['home'], '/home')

    def test_add_route_with_multiple_verbs(self):
        container = Container()
        router = Router(container)
        router.add_route(['GET', 'POST'],'/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['GET/home'], {'method': 'GET', 'uri': '/home', 'action': 'test@test'})
        self.assertEqual(routes['POST/home'], {'method': 'POST', 'uri': '/home', 'action': 'test@test'})

    def test_add_route_with_head_verb(self):
        container = Container()
        router = Router(container)
        router.head('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['HEAD/home'], {'method': 'HEAD', 'uri': '/home', 'action': 'test@test'})

    def test_add_route_with_get_verb(self):
        container = Container()
        router = Router(container)
        router.get('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['GET/home'], {'method': 'GET', 'uri': '/home', 'action': 'test@test'})

    def test_add_route_with_post_verb(self):
        container = Container()
        router = Router(container)
        router.post('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['POST/home'], {'method': 'POST', 'uri': '/home', 'action': 'test@test'})

    def test_add_route_with_put_verb(self):
        container = Container()
        router = Router(container)
        router.put('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['PUT/home'], {'method': 'PUT', 'uri': '/home', 'action': 'test@test'})

    def test_add_route_with_patch_verb(self):
        container = Container()
        router = Router(container)
        router.patch('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['PATCH/home'], {'method': 'PATCH', 'uri': '/home', 'action': 'test@test'})

    def test_add_route_with_delete_verb(self):
        container = Container()
        router = Router(container)
        router.delete('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['DELETE/home'], {'method': 'DELETE', 'uri': '/home', 'action': 'test@test'})

    def test_add_route_with_options_verb(self):
        container = Container()
        router = Router(container)
        router.options('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['OPTIONS/home'], {'method': 'OPTIONS', 'uri': '/home', 'action': 'test@test'})

    def test_add_group_routes(self):
        container = Container()
        router = Router(container)

        # Using group decorator
        @router.group({
            "middleware": "auth",
            'before':'auth',
            'namespace': 'admin',
            'domain': '{account}.myapp.com',
            'prefix': 'admin'
        })
        def group(_router):
            _router.get('/home', 'action@home')
            _router.post('/about', 'action@about')

        routes = router.get_routes()
        print(router.group_stack)
        self.assertEqual(routes['GET/home'], {'method': 'GET', 'uri': '/home', 'action': 'action@home'})
        self.assertEqual(routes['POST/about'], {'method': 'POST', 'uri': '/about', 'action': 'action@about'})

if __name__ == '__main__':
    unittest.main()
