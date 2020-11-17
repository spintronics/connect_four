import requests
from concurrent.futures import ThreadPoolExecutor
from server import ResponseCodes


def get(path = '', dictionary = {}):
    """
    . seperated lensing
    state.get('a.b.c') = state.__state['a']['b']['c']
    will retrun None if a key is encountered that doesn't exist
    """
    keys = [key for key in path.split('.') if key]
    target = dictionary
    for key in keys:
        # this doesn't accomodate lists
        if key in target:
            target = target[key]
        else:
            target = None
            break
    return target

def path_set(path, value, dictionary):
    keys = [key for key in path.split('.') if key]
    if not (len(keys)):
        return
    target = dictionary
    for key in keys[:-1]:
        if key in target:
            target = target[key]
        else:
            target = None
            break
    if target:
        target[keys[-1]] = value


class AsyncRequestPool:
    def __init__(self, host='http://127.0.0.1:5000'):
        self.executor = ThreadPoolExecutor()
        self.queue = []
        self.host = host

    def __request(self, url, data, handler = lambda x: x):
        try:
            response = requests.post(self.host + url, json=data)
            return {
                'data': response.json(),
                'url': url,
                'handler': handler,
            }
        except Exception as e:
            return {
                'url': url,
                'handler': handler,
                'data': {'code': ResponseCodes.error, 'data': str(e)},
            }

    def request(self, url, data, handler = lambda x: x):
        self.queue.append(self.executor.submit(self.__request, url, data, handler))

    def drain(self):
        try:
            done = []
            not_done = []
            for request in self.queue:
                if request.done():
                    done.append(request.result())
                else:
                    not_done.append(request)
            self.queue = not_done

            for response in done:
                response['handler'](response['data'])

            return done

        except Exception as e:
            print(e)
            return []

    def shutdown(self):
        self.executor.shutdown()

