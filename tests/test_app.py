"""
Unit tests for Flask application configuration and setup.
"""
import pytest
from app import create_app, db


class TestAppConfiguration:
    """Test cases for Flask app configuration."""
    
    def test_app_creation(self):
        """Test that app can be created."""
        app = create_app()
        assert app is not None
        assert app.name == 'app'
    
    def test_testing_config(self, app):
        """Test that testing config is set."""
        assert app.config['TESTING'] is True
        assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
    
    def test_static_bearer_token_default(self):
        """Test default static bearer token."""
        app = create_app()
        assert app.config['STATIC_BEARER_TOKEN'] == 'secret-token'
    
    def test_static_bearer_token_custom(self):
        """Test custom static bearer token via config."""
        import os
        os.environ['STATIC_BEARER_TOKEN'] = 'custom-token'
        app = create_app()
        assert app.config['STATIC_BEARER_TOKEN'] == 'custom-token'
        # Clean up
        del os.environ['STATIC_BEARER_TOKEN']
    
    def test_database_uri_from_env(self):
        """Test database URI can be set from environment."""
        import os
        test_uri = 'postgresql://test:test@localhost/test'
        os.environ['DATABASE_URL'] = test_uri
        app = create_app()
        assert app.config['SQLALCHEMY_DATABASE_URI'] == test_uri
        # Clean up
        del os.environ['DATABASE_URL']
    
    def test_sqlalchemy_track_modifications_disabled(self, app):
        """Test that SQLALCHEMY_TRACK_MODIFICATIONS is disabled."""
        assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False
    
    def test_database_tables_created(self, app):
        """Test that database tables are created on app creation."""
        with app.app_context():
            # Check if blacklists table exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            assert 'blacklists' in tables
    
    def test_api_routes_registered(self, app):
        """Test that API routes are registered."""
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert '/blacklists' in rules
        assert '/blacklists/<string:email>' in rules
    
    def test_app_has_json_support(self, client):
        """Test that app can handle JSON requests."""
        response = client.get('/blacklists/test@example.com')
        # Should get 401 (auth error) but shows JSON is supported
        assert response.content_type == 'application/json'


class TestDatabaseConnection:
    """Test cases for database connection and operations."""
    
    def test_database_session_available(self, app):
        """Test that database session is available."""
        with app.app_context():
            assert db.session is not None
    
    def test_database_operations(self, app):
        """Test basic database operations."""
        with app.app_context():
            from app.models import Blacklist
            
            # Create
            entry = Blacklist(email='dbtest@example.com')
            db.session.add(entry)
            db.session.commit()
            
            # Read
            found = Blacklist.query.filter_by(email='dbtest@example.com').first()
            assert found is not None
            assert found.email == 'dbtest@example.com'
            
            # Delete
            db.session.delete(found)
            db.session.commit()
            
            # Verify deletion
            not_found = Blacklist.query.filter_by(email='dbtest@example.com').first()
            assert not_found is None


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_404_on_invalid_route(self, client):
        """Test 404 error on invalid route."""
        response = client.get('/invalid-route')
        assert response.status_code == 404
    
    def test_405_on_wrong_method(self, client, auth_headers):
        """Test 405 error on wrong HTTP method."""
        # Try DELETE on POST-only endpoint
        response = client.delete('/blacklists', headers=auth_headers)
        assert response.status_code == 405
    
    def test_json_error_responses(self, client):
        """Test that errors return JSON responses."""
        response = client.get('/blacklists/test@example.com')
        assert response.status_code == 401
        assert response.content_type == 'application/json'
        assert 'msg' in response.json
