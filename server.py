
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from datetime import datetime, timezone
import json
import re
import uuid

BASE = Path(__file__).resolve().parent
DATA_FILE = BASE / "registrations.jsonl"


class Handler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE), **kwargs)

    # Display every browser request in the terminal
    def log_message(self, format, *args):
        print("[SERVER REQUEST]", format % args, flush=True)

    def do_POST(self):

        print("\n[POST RECEIVED]", self.path, flush=True)

        if self.path != "/api/register":
            return self.respond(404, {"error": "not_found"})

        content_type = self.headers.get("Content-Type", "")

        if content_type.split(";")[0].strip() != "application/json":
            return self.respond(415, {"error": "unsupported_media_type"})

        try:
            size = int(self.headers.get("Content-Length", "0"))

            if size <= 0 or size > 10000:
                return self.respond(413, {"error": "invalid_size"})

            data = json.loads(self.rfile.read(size))

            if not isinstance(data, dict):
                raise ValueError("Invalid data")

        except (ValueError, json.JSONDecodeError):
            return self.respond(400, {"error": "invalid_json"})

        required_fields = ["full_name", "email", "company", "message"]

        invalid_fields = [
            field for field in required_fields
            if not isinstance(data.get(field), str)
            or not data[field].strip()
        ]

        email = data.get("email", "")

        if isinstance(email, str) and not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()
        ):
            invalid_fields.append("email")

        if data.get("consent") is not True:
            invalid_fields.append("consent")

        if invalid_fields:
            return self.respond(422, {
                "error": "validation_failed",
                "fields": sorted(set(invalid_fields))
            })

        request_id = "REQ-" + uuid.uuid4().hex[:8].upper()

        record = {
            "request_id": request_id,
            "full_name": data["full_name"].strip(),
            "email": email.strip(),
            "company": data["company"].strip(),
            "message": data["message"].strip(),
            "consent": True,
            "submitted_at": datetime.now(timezone.utc).isoformat()
        }

        try:
            with DATA_FILE.open("a", encoding="utf-8") as file:
                file.write(json.dumps(record, ensure_ascii=False) + "\n")
                file.flush()

        except OSError as error:
            print("[SAVE ERROR]", error, flush=True)
            return self.respond(500, {"error": "save_failed"})

        print("[SUCCESSFULLY SAVED]", request_id, flush=True)
        print("[FILE LOCATION]", DATA_FILE, flush=True)

        return self.respond(201, {
            "status": "received",
            "request_id": request_id
        })

    def respond(self, status, obj):

        body = json.dumps(obj).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)


if __name__ == "__main__":

    print("STAR MANUFACTURING SERVER STARTING", flush=True)
    print("Website: http://127.0.0.1:8765/", flush=True)
    print("Data file:", DATA_FILE, flush=True)

    server = ThreadingHTTPServer(
        ("127.0.0.1", 8765),
        Handler
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.", flush=True)
    finally:
        server.server_close()
