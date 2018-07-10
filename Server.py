from CGIHTTPServer import CGIHTTPRequestHandler
import BaseHTTPServer

class CORSRequestHandler (CGIHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    #def end_headers(self):
    #    self.send_header('Access-Control-Allow-Origin', '*')
    #    CGIHTTPRequestHandler.end_headers(self)

if __name__=='__main__':
    BaseHTTPServer.test(HandlerClass=CORSRequestHandler)