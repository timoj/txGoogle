'''
Created on 6 okt. 2014

@author: sjuul
'''
from txGoogle.request import Request
from txGoogle.responseHandler import ResponseHandler
from txGoogle.service import Service


class Resource(object):

    def __init__(self, service, conn, *args, **kwargs):
        assert isinstance(service, Service)
        self._conn = conn
        self._service = service
        if 'requestCls' in kwargs:
            self._requestCls = kwargs['requestCls']
        else:
            self._requestCls = Request
        if 'responseCls' in kwargs:
            self._responseCls = kwargs['responseCls']
        else:
            self._responseCls = ResponseHandler

    def _request(self, requestParams):
        responseHandler = self._responseCls(self._conn, requestParams.pop('resultType'))
        reqObj = self._requestCls(**requestParams)
        self._conn.request(reqObj, responseHandler)
        return responseHandler.dfd
