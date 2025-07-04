from app import app

# Remove the __main__ block since Gunicorn will handle the server
application = app