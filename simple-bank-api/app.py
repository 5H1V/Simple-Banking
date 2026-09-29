from flask import Flask
from controllers.user_controller import user_controller
from controllers.account_controller import account_controller
from controllers.transaction_controller import transaction_controller

app = Flask(__name__)

app.register_blueprint(user_controller, url_prefix="/api")

app.register_blueprint(account_controller, url_prefix="/api")

app.register_blueprint(transaction_controller, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)