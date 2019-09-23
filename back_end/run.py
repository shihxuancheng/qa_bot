import os
from bot_app import app
port = os.environ.get('FLASK_EXPOSE_PORT')
port = port if port != None else 8080
app.run(host='0.0.0.0', port=port)