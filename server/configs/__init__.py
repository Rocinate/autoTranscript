import os


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_FOLDER = os.path.join(ROOT, 'dist')
STATIC_FOLDER = os.path.join(ROOT, 'dist/static')
UPLOAD_FOLDER = os.path.join(ROOT, 'uploads')

SECRET_KEY = "VaFGYCT7A8QYkQVS"
DATA_BASE = "mysql://root:password@172.31.35.62/chatroom"