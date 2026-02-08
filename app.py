import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from database import db
from routes.content import content_bp
from routes.auth import auth_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# ---------------- CORS ----------------
allowed_origins = [
    "http://localhost:3000",
    "https://varasa-main-six.vercel.app/"  # CHANGE to your Vercel URL later
]

CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)

# ---------------- DATABASE ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ---------------- UPLOAD FOLDER ----------------
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# create uploads folder if missing
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- JWT CONFIG ----------------
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "change-this-in-production")
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

jwt = JWTManager(app)

# ---------------- INIT DATABASE ----------------
db.init_app(app)
with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------
app.register_blueprint(content_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")

# ---------------- SERVE IMAGES ----------------
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ---------------- HEALTH CHECK (IMPORTANT FOR RENDER) ----------------
@app.route("/")
def home():
    return "Backend running"

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
