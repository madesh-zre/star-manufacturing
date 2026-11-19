import json, threading, unittest, urllib.request, urllib.error
from http.server import ThreadingHTTPServer
from server import Handler
class APITests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=ThreadingHTTPServer(('127.0.0.1',0), Handler);cls.port=cls.server.server_address[1]
  cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
 @classmethod
 def tearDownClass(cls): cls.server.shutdown();cls.server.server_close()
 def req(self,payload):
  req=urllib.request.Request(f'http://127.0.0.1:{self.port}/api/register',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
  try:
   with urllib.request.urlopen(req) as x:return x.status,json.loads(x.read())
  except urllib.error.HTTPError as x:return x.code,json.loads(x.read())
 def test_valid_request(self):
  code,body=self.req({'full_name':'Sample Customer','email':'customer@example.test','company':'Sample Industries','message':'Prototype requirements','consent':True});self.assertEqual(code,201);self.assertEqual(body['status'],'received')
 def test_missing_consent(self):
  code,body=self.req({'full_name':'Sample Customer','email':'customer@example.test','company':'Sample Industries','message':'Prototype requirements','consent':False});self.assertEqual(code,422);self.assertIn('consent',body['fields'])
 def test_bad_email(self):
  code,body=self.req({'full_name':'Sample Customer','email':'invalid','company':'Sample Industries','message':'Prototype requirements','consent':True});self.assertEqual(code,422);self.assertIn('email',body['fields'])
if __name__=='__main__':unittest.main()
