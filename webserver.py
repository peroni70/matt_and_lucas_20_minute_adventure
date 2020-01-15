from http.server import HTTPServer, CGIHTTPRequestHandler, BaseHTTPRequestHandler
import cgi
from PIL import Image
from io import BytesIO
class echoHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
        content_len = int(self.headers.get('Content-length'))
        pdict['CONTENT-LENGTH'] = content_len
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            my_image = bytes(fields.get('image')[0])
            image = Image.open(BytesIO(my_image))
            image.show()
            self.send_response(200)
def main():
    PORT = 8080
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, echoHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()