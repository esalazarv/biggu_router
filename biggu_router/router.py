class Router:
    def __init__(self, app):
        self.app = app
        self.group_stack = {}
        self.routes = {}
        self.named_routes = {}

    def group(self, attributes):
        def wrapper(func):
            if 'middleware' in attributes and type(attributes['middleware']) == str:
                attributes['middleware'] = attributes['middleware'].split('|')
            self.update_group_stack(attributes)
            func(self)
            # TODO: POP last item in group stack
        return wrapper

    def update_group_stack(self, attributes):
        if not self.group_stack:
            attributes = self.merge_with_last_group(attributes)
        self.group_stack = attributes

    def merge_with_last_group(self, new):
        items = list(self.group_stack.items())
        key, values = items.pop() if items else [None, {}]
        return self.merge_group(new, values)

    def merge_group(self, new, old):
        # TODO: add namespace build
        new['namespace'] = ''
        # TODO: add prefix build
        new['prefix'] = ''
        if 'domain' in new:
            old.pop('domain', None)

        if 'as' in old:
            complement = '.' + new['as'] if 'as' in new else ''
            new['as'] = old['as'] + complement

        if 'suffix' in old and 'suffix' not in new:
            new['suffix'] = old['suffix']

        filtered = filter(lambda item: item[0] in ['namespace', 'prefix', 'as', 'suffix'], old.items())
        result = { key : value for key,value in filtered }
        return self.merge_recursive(result, new)

    def merge_recursive(self, target, source):
        for key, value in source.items():
            if isinstance(value, dict):
                node = target.setdefault(key, {})
                self.merge_recursive(value, node)
            else:
                target[key] = value
        return target

    def add_route(self, method, uri, action):

        uri = '/' + uri.strip('/')

        if type(action) == dict and 'as' in action:
            self.named_routes[action['as']] = uri

        if type(method) == list:
            for verb in method:
                self.routes[verb + uri] = {'method': verb, 'uri': uri, 'action': action}
        else:
            self.routes[method + uri] = { 'method': method,  'uri': uri, 'action': action }

    def head(self, uri, action):
        self.add_route('HEAD', uri, action)
        return self

    def get(self, uri, action):
        self.add_route('GET', uri, action)
        return self

    def post(self, uri, action):
        self.add_route('POST', uri, action)
        return self

    def put(self, uri, action):
        self.add_route('PUT', uri, action)
        return self

    def patch(self, uri, action):
        self.add_route('PATCH', uri, action)
        return self

    def delete(self, uri, action):
        self.add_route('DELETE', uri, action)
        return self

    def options(self, uri, action):
        self.add_route('OPTIONS', uri, action)
        return self

    def get_routes(self):
        return self.routes

