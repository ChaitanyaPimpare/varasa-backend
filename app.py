import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from database import db
from routes.content import content_bp
from routes.auth import auth_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# ---------- CORS (React can talk to Flask) ----------
CORS(
    app,
    resources={r"/api/*": {"origins": "http://localhost:3000"}},
    supports_credentials=True
)

# ---------- DATABASE ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ---------- UPLOAD FOLDER ----------
app.config["UPLOAD_FOLDER"] = "uploads"

# ---------- JWT CONFIG ⭐ (THIS WAS MISSING) ----------
app.config["JWT_SECRET_KEY"] = "super-secret-key-please-change"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

jwt = JWTManager(app)

# ---------- INIT DATABASE ----------
db.init_app(app)
with app.app_context():
    db.create_all()

# ---------- REGISTER ROUTES ----------
app.register_blueprint(content_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")

# ---------- SERVE IMAGES ----------
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
