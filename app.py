from flask import Flask, Response, request
import requests

app = Flask(__name__)

TARGET_URL = "https://venya76.github.io/mines/"

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def proxy(path):
    url = TARGET_URL + path
    resp = requests.get(url, params=request.args)

    excluded_headers = ["content-encoding", "transfer-encoding", "connection"]
    headers = [(name, value) for (name, value) in resp.headers.items() if name.lower() not in excluded_headers]

    # Убираем X-Frame-Options и CSP
    headers = [(name, value) for (name, value) in headers
               if "frame" not in name.lower() and "content-security-policy" not in name.lower()]
    headers.append(("X-Frame-Options", "ALLOWALL"))

    return Response(resp.content, resp.status_code, headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
