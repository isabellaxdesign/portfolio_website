import http.server
import socketserver

PORT = 5000

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def send_response_only(self, code, message=None):
        super().send_response_only(code, message)

    def send_head(self):
        # Strip conditional request headers so we never return 304
        self.headers._headers = [
            h for h in self.headers._headers
            if h[0].lower() not in ("if-modified-since", "if-none-match")
        ]
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), NoCacheHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
