from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import re

@dispatcher.add_method
def echo(*args, **kwargs):
    print(args, kwargs)
    return args

@dispatcher.add_method
def parse_log(log):
    lines = log.split('\n')
    category_counter = dict()
    matches = matcher.finditer(log)
    file_length = len(log.splitlines())
    matches_length = 0
    for match in matches:
        matches_length += 1
        key_string = ''
        if match.group(2) == 'for':
            key_string = match.group(1)
        else:
            separated_string = match.group(1).split(' ')
            if len(separated_string) > 1:
                key_string = (' ').join(separated_string[:-1])
            else:
                key_string = separated_string[0]

        if key_string in category_counter:
            category_counter[key_string] += 1
        else:
            category_counter[key_string] = 1

    category_counter["Unidentified"] = file_length - matches_length
    return category_counter

@Request.application
def application(request):
    # print(request.data)
    dispatcher["echo"] = lambda s: s
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype = 'application/json')

if __name__ == '__main__':
    matcher = re.compile('\[\d+\]: (.+?) (for|from)')
    run_simple('127.0.0.1', 8080, application)
