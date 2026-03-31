"""Basic tests for the Stock Dashboard API"""

import pytest


def test_basic_import():
    """Test that the app module can be imported"""
    try:
        from app import main
        assert True
    except ImportError:
        pytest.fail("Failed to import app module")


def test_app_initialization():
    """Test that the FastAPI app initializes"""
    try:
        from app.main import app
        assert app is not None
    except Exception as e:
        pytest.fail(f"Failed to initialize app: {e}")
