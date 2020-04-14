class Router:
    def __init__(self, app):
        self.app = app
        self.group_stack = []
        self.routes = {}
        self.named_routes = {}

    def group(self, attributes):
        def wrapper(func):
            if 'middleware' in attributes and type(attributes['middleware']) == str:
                attributes['middleware'] = attributes['middleware'].split('|')
            self.update_group_stack(attributes)
            func(self)
            self.group_stack.pop()
        return wrapper

    def update_group_stack(self, attributes):
        if self.has_group_stack():
            attributes = self.merge_with_last_group(attributes)
        self.group_stack.append(attributes)

    def merge_with_last_group(self, new):
        items = self.group_stack
        values = items[-1] if items else {}
        return self.merge_group(new, values)

    def merge_group(self, new, old):
        new['namespace'] = self.format_uses_prefix(new, old)
        new['prefix'] = self.format_group_prefix(new, old)
        if 'domain' in new:
            old.pop('domain', None)

        if 'as' in old:
            complement = '.' + new['as'] if 'as' in new else ''
            new['as'] = old['as'] + complement

        if 'suffix' in old and 'suffix' not in new:
            new['suffix'] = old['suffix']

        filtered = filter(lambda item: item[0] not in ['namespace', 'prefix', 'as', 'suffix'], old.items())
        result = { key : value for key,value in filtered }
        return self.merge_recursive(result, new)

    @staticmethod
    def format_uses_prefix(new, old):
        if 'namespace' in new:
            if 'namespace' in old and new['namespace'].find('.') != -1:
                return old['namespace'].strip('.') + '.' + new['namespace'].strip('.')
            else:
                return  new['namespace'].strip('.')
        return old['namespace'] if 'namespace' in old else None

    @staticmethod
    def format_group_prefix(new, old):
        if 'prefix' in old:
            old_prefix = old['prefix']
        else:
            old_prefix = None

        if 'prefix' in new:
            if old_prefix:
                return old_prefix.strip('/') + '/' + new['prefix'].strip('/')
            else:
                return '/' + new['prefix'].strip('/')

        return old_prefix

    def merge_recursive(self, target, source):
        for key, value in source.items():
            if isinstance(value, dict):
                node = target.setdefault(key, {})
                self.merge_recursive(value, node)
            else:
                target[key] = value
        return target

    def add_route(self, method, uri, action):
        action = self.parse_action(action)
        attributes = None
        if self.has_group_stack():
            attributes = self.merge_with_last_group({})

        if type(attributes) == dict:
            if 'prefix' in attributes and attributes['prefix']:
                uri = attributes['prefix'].strip('/') + '/' + uri.strip('/')

            if 'suffix' in attributes and attributes['suffix']:
                uri = uri.strip('/') + '/' + attributes['suffix'].strip('/')

            action = self.merge_group_attributes(action, attributes)

        uri = '/' + uri.strip('/')

        if type(action) == dict and 'as' in action:
            self.named_routes[action['as']] = uri

        if type(method) == list:
            for verb in method:
                self.routes[verb + uri] = {'method': verb, 'uri': uri, 'action': action}
        else:
            self.routes[method + uri] = { 'method': method,  'uri': uri, 'action': action }

    @staticmethod
    def parse_action(action):
        if type(action) == str:
            return {'uses': action}
        elif type(action) != dict:
            return {action}

        if 'middleware' in action and type(action['middleware']) == str:
            action['middleware'] = action['middleware'].split('|')

        return action

    # Merge current route attributes (namespace, middleware and alias) with group attributes
    def merge_group_attributes(self, action, attributes):
        namespace = attributes['namespace'] if 'namespace' in attributes else None
        middleware = attributes['middleware'] if 'middleware' in attributes else None
        alias = attributes['as'] if 'as' in attributes else None

        grouped_aliases = self.merge_alias_group(action, alias)
        grouped_middleware = self.merge_middleware_group(grouped_aliases, middleware)
        return self.merge_namespace_group(grouped_middleware, namespace)

    # If group has middleware list then merge current route middleware list with previous group list
    @staticmethod
    def merge_middleware_group(action, middleware = None):
        if type(middleware) == list:
            if 'middleware' in action:
                # spread the group middleware list in to a temporal list
                list_middleware = [*middleware]
                # combine unique values keeping order (other merge techniques not do it)
                [list_middleware.append(item) for item in action['middleware'] if item not in list_middleware]
                action['middleware'] = list_middleware
            else:
                action['middleware'] = middleware
        return action

    @staticmethod
    def merge_alias_group(action, alias = None):
        if alias:
            if 'as' in action:
                action['as'] = alias + '.' + action['as']
            else:
                action['as'] = alias
        return action

    def merge_namespace_group(self, action, namespace):
        if namespace and 'uses' in action:
            action['uses'] = self.prepend_group_namespace(action['uses'], namespace)
        return action

    @staticmethod
    def prepend_group_namespace(class_name, namespace):
        return namespace + '.' + class_name if namespace and class_name.find('.') != 0 else class_name

    def has_group_stack(self):
        return len(self.group_stack) != 0

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

