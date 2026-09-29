from flask import Flask
from controllers.customer_controller import customer_controller

app = Flask(__name__)

app.register_blueprint(
    customer_controller,
    url_prefix="/api"
    )

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
