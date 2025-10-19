"""
AWS Elastic Beanstalk entry point.
EBS expects a file named 'application.py' with an 'application' variable.
"""
from app import create_app, db

# Create the application instance
application = create_app()

# Automatically create tables if they don't exist
with application.app_context():
    db.create_all()
    print('Database tables ready')

if __name__ == '__main__':
    # For local testing only - EBS will use gunicorn
    application.run(host='0.0.0.0', port=8080)
