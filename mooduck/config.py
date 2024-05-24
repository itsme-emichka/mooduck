import os

from dotenv import load_dotenv


load_dotenv()

# DATABASE
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')

# SETTINGS
SECRET_KEY = os.getenv('SECRET_KEY')

# REGEX_PATTERNS
SLUG_PATTERN: str = r'^[-_a-z0-9]*$'
EMAIL_PATTERN: str = r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+'
BASE64_PATTERN: str = r'^data:image/(png|jpeg|jpg);base64,.+$'
HEX_PATTERN: str = r'^#[a-z0-9]{6}$'
PHONE_NUMBER: str = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
ROLE_CHOICES_PATTERN: str = r'^(admin|moder|user)$'

# TOKEN
ACCESS_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"
TOKEN_TYPE: str = 'Bearer'
