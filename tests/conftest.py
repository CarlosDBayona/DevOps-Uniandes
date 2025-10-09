"""
Test configuration and fixtures for Flask Blacklist API tests.
"""
import pytest
from app import create_app, db
from app.models import Blacklist


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'STATIC_BEARER_TOKEN': 'test-token'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Return valid authorization headers."""
    return {
        'Authorization': 'Bearer test-token',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_blacklist(app):
    """Create sample blacklist entries in the database."""
    with app.app_context():
        entries = [
            Blacklist(
                email='blocked1@example.com',
                app_uuid='app-001',
                blocked_reason='spam'
            ),
            Blacklist(
                email='blocked2@example.com',
                app_uuid='app-002',
                blocked_reason='abuse'
            ),
            Blacklist(
                email='duplicate@example.com',
                app_uuid='app-003',
                blocked_reason='first entry'
            ),
            Blacklist(
                email='duplicate@example.com',
                app_uuid='app-004',
                blocked_reason='second entry - most recent'
            ),
        ]
        for entry in entries:
            db.session.add(entry)
        db.session.commit()
        yield entries
