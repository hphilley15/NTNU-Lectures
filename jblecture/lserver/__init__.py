import portpicker
import threading
import http.server
import socketserver
from .jbcd import JBcd

port = portpicker.pick_unused_port()

class V6Server(socketserver.TCPServer):
  address_family = socket.AF_INET6

def startLocalServer( ):
    def server_entry():
        if ( cfg['HTTPD'] ):
            stopLocalServer()
        cfg['HTTPD'] = None
        handler = http.server.SimpleHTTPRequestHandler
        port = portpicker.pick_unused_port()
        with JBcd( cfg['REVEAL_DIR'] ):
            with V6Server(("::", port), handler) as httpd:
                print("serving at port", port)
                cfg['HTTPD'] = httpd
                httpd.serve_forever()

    cfg['HTTPD'] = None
    cfg['HTTP_PORT'] = port
    thread = threading.Thread( target=server_entry )
    thread.daemon = True
    thread.start()
