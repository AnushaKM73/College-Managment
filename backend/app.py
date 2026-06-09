from flask import Flask
from flask_cors import CORS

from routes.auth import auth_bp
from routes.student import student_bp
from routes.admin import admin_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return {
        "message":"College Management API Running"
    }

if __name__ == "__main__":
    app.run(debug=True)