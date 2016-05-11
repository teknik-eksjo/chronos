import os
from app import create_app


app = create_app(os.getenv('CHRONOS_CONFIG') or 'default')
