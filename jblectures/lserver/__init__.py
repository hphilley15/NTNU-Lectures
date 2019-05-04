import portpicker
import threading
import http.server
import socketserver

port = portpicker.pick_unused_port()

def server_entry():
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()

thread = threading.Thread( target=server_entry )
#thread.start()
