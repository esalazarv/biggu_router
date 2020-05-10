import regex
from .bad_route_exception import BadRouteException

class RouteParser:
    PATTERN = r"\{\s*([a-zA-Z_][a-zA-Z0-9_-]*)\s*(?::\s*([^{}]*(?:\{(?2)\}[^{}]*)*))?\}"
    DEFAULT_DISPATCH_REGEX = r'[^/]+'

    def parse(self, route: str):
        # Check if the given route has not closings
        route_without_closing_optionals = route.rstrip(']')
        num_optionals = len(route) - len(route_without_closing_optionals)

        # Get matches as list
        parts = regex.split(RouteParser.PATTERN + r'(*SKIP)(*FAIL)|\[', route_without_closing_optionals)

        # Remove empty matches
        segments = [segment for segment in parts if segment != None]

        # Raise Exception if route has not closings or if optionals are not in the end of route
        if num_optionals != len(segments) -1 :
            match = regex.search(RouteParser.PATTERN + r'(*SKIP)(*FAIL)|\]', route_without_closing_optionals)
            if match:
                raise BadRouteException('Optional segments can only occur at the end of a route')
            raise BadRouteException("Number of opening '[' and closing ']' does not match")    

        current_route = ''
        route_data = []
        
        # Get route data for each segment
        for index,segment in enumerate(segments):
            if segments == '' and index != 0:
                raise BadRouteException('Empty optional segment')
            current_route += segment
            route_data.append(self.parse_placeholders(current_route))  
        return route_data 

    def parse_placeholders(self, route:str):
        matches = regex.findall(RouteParser.PATTERN, route)
        # If not found matches then return current route
        if not matches:
            return [route]

        offset = 0
        route_data = []

        # Remove empty matches
        mapped = list(map(lambda match: [item for item in match if len(item)], matches))
        for match in mapped:
            # Find the matches with params for get its position and update offset
            param_pattern = RouteParser.PATTERN
            param_match = regex.search(param_pattern, route, pos=offset)
            pos = offset
            param = match[0]
            # If match then get position and append the first part of route to the route data
            if param_match:
                span = param_match.span()
                pos = span[0]
                param = param_match[0]
                if pos > offset:
                    route_data.append(route[offset: pos])
             
            # Append segments and found params      
            route_data.append([
                match[0],
                match[1].strip() if len(match[1:]) else RouteParser.DEFAULT_DISPATCH_REGEX,
            ])

            # Update the offset for the next iteration
            offset = pos + len(param)
           
        #append the rest of the route segment   
        if offset != len(route):
            route_data.append(route[offset:])
        return route_data