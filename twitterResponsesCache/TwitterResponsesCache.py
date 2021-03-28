import json
import base64


class TwitterResponsesCache:

    def __init__(self, cacheFileName=None):
        if not cacheFileName:
            raise Exception('The Twitter Responses Cache requires path for a '
                            'cache file.')
        self.cacheFileName = cacheFileName
        self.cacheFile = open(cacheFileName, 'rw')
        self.cache = []

    def execute(self, obj, funcName, *args, **kwargs):
        callInfo = {'objClassName': type(obj).__name__,
                    'funcName': funcName,
                    'args': args,
                    'kwargs': kwargs}
        callInfoJson = json.dumps(callInfo)
        callInfoBase64 = base64.encodebytes(callInfoJson.encode())
        if callInfoBase64 in self.cache:
            pass
        retVal = getattr(obj, funcName)(*args, **kwargs)
        return retVal
