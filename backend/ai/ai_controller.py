from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from .ai_service import ask_ai

class AIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/ai/chat":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            user_message = data.get("message", "")
            ai_response = ask_ai(user_message)

            response = json.dumps({"response": ai_response}).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response)

def run_ai_server():
    server = HTTPServer(("0.0.0.0", 8000), AIHandler)
    print("AI server running on port 8000")
    server.serve_forever()

if __name__ == "__main__":
    run_ai_server()