import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to a known state before each test"""
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 2,
            "participants": ["emma@mergington.edu"]
        },
        "Full Activity": {
            "description": "Test activity at capacity",
            "schedule": "Mondays, 2:00 PM - 3:00 PM",
            "max_participants": 1,
            "participants": ["john@mergington.edu"]
        }
    }
    
    # Clear and repopulate
    activities.clear()
    activities.update(original_activities)
    
    yield activities
    
    # Cleanup
    activities.clear()
    activities.update(original_activities)
