from dotenv import load_dotenv
import os

# Initialize MySQL credentials from the environment variables we just loaded.
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DB = os.environ.get("DB_DB")  # database to use.

# Load environment variables from .env file.
load_dotenv()

class Config:
    # Secret key for preventing CSRF attacks.
    SECRET_KEY = "placeholder"
    # initializes email configuration variables
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    GOOGLE_ID = os.environ.get("GOOGLE_ID")
    GOOGLE_SECRET = os.environ.get("GOOGLE_SECRET")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # Set up SQLAlchemy with the above credentials.
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"