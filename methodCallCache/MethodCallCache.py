import json
import base64


class MethodCallCache:

    def __init__(self, cacheFileName=None):
        if not cacheFileName:
            raise Exception('The Method Call Cache requires path for a '
                            'cache file.')
        self.cacheFileName = cacheFileName
        self.timeToWrite = 0
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
            # print('Loaded from cache: ', retVal)
            return retVal
        retVal = getattr(obj, funcName)(*args, **kwargs)
        retValJson = json.dumps(retVal)
        retValBase64 = base64.encodebytes(retValJson.encode()).decode()
        self.cache[callInfoBase64] = str(retValBase64)
        # print('Saved to cache: ', retVal)
        self.timeToWrite += 1
        if self.timeToWrite == 256:
            self.forceCacheDump()
        return retVal

    def checkIfCached(self, obj, funcName, *args, **kwargs):
        callInfo = {'objClassName': type(obj).__name__,
                    'funcName': funcName,
                    'args': args,
                    'kwargs': kwargs}
        callInfoJson = json.dumps(callInfo)
        callInfoBase64 = base64.encodebytes(callInfoJson.encode()).decode()
        if callInfoBase64 in self.cache:
            return True
        return False

    def forceCacheDump(self):
        cacheToWrite = json.dumps(self.cache)
        self.cacheFile.seek(0)
        self.cacheFile.truncate()
        self.cacheFile.write(cacheToWrite)
        self.timeToWrite = 0
        print('Cache has been dumped to file.')
