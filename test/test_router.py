import unittest
from biggu_container import Container
from biggu_router import Router


class RouterTest(unittest.TestCase):
    def test_add_route(self):
        container = Container()
        router = Router(container)
        router.add_route('GET', '/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['GET/home'], {
            'method': 'GET',
            'uri': '/home',
            'action': {
                'uses':'test@test'
            }
        })

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
        self.assertEqual(routes['GET/home'], {
            'method': 'GET',
            'uri': '/home',
            'action': {
                'uses': 'test@test'
            }
        })
        self.assertEqual(routes['POST/home'], {
            'method': 'POST',
            'uri': '/home',
            'action': {
                'uses': 'test@test'
            }
        })

    def test_add_route_with_head_verb(self):
        container = Container()
        router = Router(container)
        router.head('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['HEAD/home'], {
            'method': 'HEAD',
            'uri': '/home',
            'action': {
                'uses': 'test@test'
            }
        })

    def test_add_route_with_get_verb(self):
        container = Container()
        router = Router(container)
        router.get('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['GET/home'], {
            'method': 'GET',
            'uri': '/home',
            'action': {
                'uses': 'test@test'
            }
        })

    def test_add_route_with_post_verb(self):
        container = Container()
        router = Router(container)
        router.post('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['POST/home'], {
            'method': 'POST',
            'uri': '/home',
            'action': {
                'uses':'test@test'
            }
        })

    def test_add_route_with_put_verb(self):
        container = Container()
        router = Router(container)
        router.put('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['PUT/home'], {
            'method': 'PUT',
            'uri': '/home',
            'action': {
                'uses':'test@test',
            }
        })

    def test_add_route_with_patch_verb(self):
        container = Container()
        router = Router(container)
        router.patch('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['PATCH/home'], {
            'method': 'PATCH',
            'uri': '/home',
            'action': {
                'uses':'test@test'
            }
        })

    def test_add_route_with_delete_verb(self):
        container = Container()
        router = Router(container)
        router.delete('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['DELETE/home'], {
            'method': 'DELETE',
            'uri': '/home',
            'action': {
                'uses': 'test@test'
            }
        })

    def test_add_route_with_options_verb(self):
        container = Container()
        router = Router(container)
        router.options('/home', 'test@test')
        routes = router.get_routes()
        self.assertEqual(routes['OPTIONS/home'], {
            'method': 'OPTIONS',
            'uri': '/home',
            'action': {
                'uses': 'test@test'
            }
        })

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
            _router.get('/home', {
                'as' : 'home',
                'uses': 'CMSController@home'
            })
            _router.post('/about', 'CMSController@about')
            @router.group({
                "middleware": "auth",
                'before': 'auth',
                'namespace': 'users.',
                'domain': '{account}.myapp.com',
                'prefix': 'users'
            })
            def _group(_router):
                _router.get('/', {
                    'as': 'users',
                    'uses': 'UserController@index',
                    'middleware': 'permissions'
                })
                _router.get('/{id}', 'UserController@show')

        routes = router.get_routes()
        self.assertEqual(routes['GET/admin/home'], {
            'method': 'GET',
            'uri': '/admin/home',
            'action': {
                'as': 'home',
                'uses':'admin.CMSController@home',
                'middleware': ['auth']
            }
        })
        self.assertEqual(routes['POST/admin/about'], {
            'method': 'POST',
            'uri': '/admin/about',
            'action': {
                'uses': 'admin.CMSController@about',
                'middleware': ['auth']
            }
        })
        self.assertEqual(routes['GET/admin/users'], {
            'method': 'GET',
            'uri': '/admin/users',
            'action': {
                'as': 'users',
                'uses': 'admin.users.UserController@index',
                'middleware': ['auth', 'permissions']
            }
        })
        self.assertEqual(routes['GET/admin/users/{id}'], {
            'method': 'GET',
            'uri': '/admin/users/{id}',
            'action': {
                'uses': 'admin.users.UserController@show',
                'middleware': ['auth']
            }
        })

if __name__ == '__main__':
    unittest.main()
