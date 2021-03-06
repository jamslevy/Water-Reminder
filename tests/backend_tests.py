#!/usr/bin/env python

import os
import unittest
from webtest import TestApp, AppError

from google.appengine.api import apiproxy_stub_map, user_service_stub, datastore_file_stub

from backend import application
import app_settings

class BooksTest(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(application)
        os.environ['APPLICATION_ID'] = "temp"
        os.environ['USER_EMAIL'] = "test@example.com"
        os.environ['SERVER_NAME'] = "localhost"
        os.environ['SERVER_PORT'] = "8080"
        
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        apiproxy_stub_map.apiproxy.RegisterStub('user', user_service_stub.UserServiceStub())
        stub = datastore_file_stub.DatastoreFileStub('temp', '/dev/null', '/dev/null')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
    
    def test_index_returns_200(self):
        response = self.app.get('/', expect_errors=True) 
        self.assertEquals("200 OK", response.status)

    def test_index_has_correct_title(self):
        response = self.app.get('/', expect_errors=True)        
        response.mustcontain("<title>%s</title>" % app_settings.APP_TITLE)
        
    def test_index_returns_correct_mime_type(self):
        response = self.app.get('/', expect_errors=True)
        self.assertEquals(response.content_type, "text/html")

