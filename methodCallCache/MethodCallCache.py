import json
import base64


class MethodCallCache:

    def __init__(self, cacheFileName=None):
        if not cacheFileName:
            raise Exception('The Method Call Cache requires path for a '
                            'cache file.')
        self.cacheFileName = cacheFileName
        self.cache = {}
        try:
            self.cacheFile = open(cacheFileName, 'r+')
            self.cache = json.load(self.cacheFile)
        except Exception:
            self.cacheFile = open(cacheFileName, 'w+')

    def execute(self, obj, funcName, *args, **kwargs):
        callInfo = {'objClassName': type(obj).__name__,
                    'funcName': funcName,
                    'args': args,
                    'kwargs': kwargs}
        callInfoJson = json.dumps(callInfo)
        callInfoBase64 = base64.encodebytes(callInfoJson.encode()).decode()
        if callInfoBase64 in self.cache:
            retValBase64 = self.cache[callInfoBase64]
            retValJson = base64.decodebytes(retValBase64.encode())
            retVal = json.loads(retValJson)
            print('Loaded from cache.')
            return retVal
        retVal = getattr(obj, funcName)(*args, **kwargs)
        retValJson = json.dumps(retVal)
        retValBase64 = base64.encodebytes(retValJson.encode()).decode()
        self.cache[callInfoBase64] = str(retValBase64)
        cacheToWrite = json.dumps(self.cache)
        self.cacheFile.seek(0)
        self.cacheFile.truncate()
        self.cacheFile.write(cacheToWrite)
        print('Saved to cache.')
        return retVal
