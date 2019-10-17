import portpicker
import threading
import http.server
import socketserver

port = portpicker.pick_unused_port()

class V6Server(socketserver.TCPServer):
  address_family = socket.AF_INET6

def startLocalServer( ):
    def server_entry():
        if ( cfg['HTTPD'] ):
            stopLocalServer()
        cfg['HTTPD'] = None
        handler = http.server.SimpleHTTPRequestHandler
        port = int( cfg['HTTP_PORT'] )
        with jbcd.JBcd( cfg['REVEAL_DIR'] ):
            with V6Server(("::", port), handler) as httpd:
                print("serving at port", port)
                cfg['HTTPD'] = httpd
                httpd.serve_forever()

    cfg['HTTPD'] = None
    thread = threading.Thread( target=server_entry )
    thread.daemon = True
    thread.start()
