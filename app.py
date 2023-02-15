import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def blue_or_green():
    """
    This function returns if the service is running on blue or green cluster env.
    """
    return "You are being routed to tweag-dev-blue-cluster"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True,host='0.0.0.0',port=port)
