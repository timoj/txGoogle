'''
Created on 9 sep. 2014

@author: sjuul
'''
from urllib import unquote
import simplejson as json
from txGoogle.responseHandler import ResponseHandler


class GoogleResponseHandler(ResponseHandler):

    def __init__(self, *args, **kwargs):
        super(GoogleResponseHandler, self).__init__(*args, **kwargs)
        self._result = None

    def handleLoaded(self, loaded, requestObj):
        if 'error' in loaded:
            if 'errors' in loaded['error']:
                errorMessages = [item['message'] for item in loaded['error']['errors']]
                self._dfd.errback(Exception('\n'.join(errorMessages)))
            else:
                self._dfd.errback(Exception(json.dumps(loaded['error'])))
        else:
            self._onResponse(loaded, requestObj)

    def _maxResultsReached(self, requestObj):
        maxResults = requestObj.maxResults
        if maxResults and self._result is not None:
            if hasattr(self, '_getResultLen_' + self._resultType):
                curCntFun = getattr(self, '_getResultLen_' + self._resultType)
                return curCntFun() >= maxResults
            elif hasattr(self._result, '__len__'):
                return len(self._result) >= maxResults
            else:
                return False
        return False

    def _onResponse(self, loaded, requestObj):
        self._loadResults(loaded, requestObj)

        if 'nextPageToken' in loaded and not self._maxResultsReached(requestObj):
            requestObj.setUrlParam('pageToken', unquote(loaded['nextPageToken']))
            self._connection.request(requestObj, self)
        else:
            self._dfd.callback(self._result)
