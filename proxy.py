import http.server
import socketserver
import urllib.request
import os
import mimetypes

PORT = 8080
REMOTE = "https://epiminds.com"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        local_path = self.translate_path(self.path)
        # Serve index.html for root path
        if os.path.isdir(local_path):
            index_path = os.path.join(local_path, "index.html")
            if os.path.isfile(index_path):
                local_path = index_path
        if os.path.exists(local_path) and os.path.isfile(local_path):
            self.send_response(200)
            ctype, _ = mimetypes.guess_type(local_path)
            if ctype:
                self.send_header("Content-Type", ctype)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open(local_path, "rb") as f:
                self.wfile.write(f.read())
            return
        
        url = f"{REMOTE}{self.path}"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": self.headers.get("User-Agent", "Mozilla/5.0"),
                "Accept": self.headers.get("Accept", "*/*"),
                "Accept-Language": self.headers.get("Accept-Language", "*"),
                "Referer": REMOTE + "/",
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    kl = k.lower()
                    if kl not in ("transfer-encoding", "content-encoding", "connection", "keep-alive"):
                        self.send_header(k, v)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(resp.read())
        except Exception as e:
            self.send_error(404, f"Not found locally or remotely: {self.path}")
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

with socketserver.TCPServer(("127.0.0.1", PORT), ProxyHandler) as httpd:
    print(f"Proxy running at http://127.0.0.1:{PORT}")
    print(f"Serving local files, proxying missing to {REMOTE}")
    httpd.serve_forever()
