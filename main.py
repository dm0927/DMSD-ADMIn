import os
import sys
from flask import Flask, render_template
from dotenv import load_dotenv
import flask_login

load_dotenv()

# added so modules can be found between the two different lookup states:
# from tests and from regular running of the app

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURR_DIR)

login_manager = flask_login.LoginManager()
login_manager.login_view = "home.index"
login_manager.login_message = "Login to access"
login_manager.login_message_category = "warning"


def create_app(config_filename=''):
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "missing_secret")
    app.static_folder = 'static'
    with app.app_context():
        from views.index import home
        app.register_blueprint(home)
        from views.appointment import appointment
        app.register_blueprint(appointment)
        from views.vehicle import vehicle
        app.register_blueprint(vehicle)

        login_manager.init_app(app)
        @login_manager.user_loader
        def load_user(id):
            from sql.db import DB
            from auth.models import User
            try:
                result = DB.selectOne("SELECT Cust_ID as id, Name as name, Phone as phone, Email as email, Address as address FROM CUSTOMER WHERE Cust_ID = %s", id)
                if result.status:
                    return User(**result.row)
            except Exception as e:
                print(e)
            return None
        
        # @app.errorhandler(404)
        # # inbuilt function which takes error as parameter
        # def not_found(e):
        #     return render_template("404.html")
        return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
