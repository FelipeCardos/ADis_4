from flask import Flask
import ssl
app = Flask(__name__)
@app.route('/login', methods = ["GET"])
def login():
  return 'Login'
if __name__ == '__main__':
  context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
  context.verify_mode = ssl.CERT_REQUIRED
  context.load_verify_locations(cafile='root.pem')
  context.load_cert_chain(certfile='serv.crt',keyfile='serv.key')
  app.run('localhost', ssl_context=context, debug = True)
