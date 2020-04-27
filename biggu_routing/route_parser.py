import regex

class RouteParser:
    PATTERN = r"\{\s*([a-zA-Z_][a-zA-Z0-9_-]*)\s*(?::\s*([^{}]*(?:\{(.?-1)\}[^{}]*)*))?\}"
    DEFAULT_DISPATCH_REGEX = r'[^/]+'

    def parse(self, route: str):
        route_without_closing_optionals = route.rstrip(']')
        num_optionals = len(route) - len(route_without_closing_optionals)
        parts = regex.split(r'~' + RouteParser.PATTERN + r'(*SKIP)(*FAIL)|\[', route_without_closing_optionals)
        segments = [segment for segment in parts if segment]
        if num_optionals != len(segments) -1 :
            match = regex.search(r'~' + RouteParser.PATTERN + r'(*SKIP)(*FAIL)|\]', route_without_closing_optionals)
            if match:
                raise Exception('Optional segments can only occur at the end of a route')
            raise Exception("Number of opening '[' and closing ']' does not match")    

        current_route = ''
        route_data = [] 
        for index,segment in enumerate(segments):
            if segments == '' and index != 0:
                raise Exception('Empty optional segment')
            current_route += segment
            route_data.append(self.parse_placeholders(current_route))
        return route_data 

    def parse_placeholders(self, route:str):
        matches = regex.findall(RouteParser.PATTERN, route)
        
        if not matches:
            return [route]

        offset = 0
        route_data = []
        mapped = list(map(lambda match: [item for item in match if len(item)], matches))

        for match in mapped:
            param = '{' + ":".join(match) + '}'
            pos = route.find(param, offset)
            if pos > offset:
                route_data.append(route[offset: pos])
            route_data.append([
                match[0],
                match[1].strip() if len(match[1:]) else RouteParser.DEFAULT_DISPATCH_REGEX,
            ])    
            offset = pos + len(param)
           
        if offset != len(route):
            route_data.append(route[offset:])   
        return route_data