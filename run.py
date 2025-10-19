from app import create_app, db
from app.models import Blacklist


app = create_app()


@app.cli.command('create-db')
def create_db():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print('Created database tables')


if __name__ == '__main__':
    # Automatically create tables if they don't exist
    with app.app_context():
        db.create_all()
        print('Database tables ready')
    
    app.run(host='0.0.0.0', port=8080)
