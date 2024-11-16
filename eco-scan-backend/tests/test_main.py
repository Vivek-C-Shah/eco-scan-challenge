# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from carbon_scores import CARBON_SCORES
from offers import OFFERS
from utils import calculate_reward_points
import io
from PIL import Image

client = TestClient(app)

# Testing /analyze-image endpoint

def test_analyze_image_success():
    # Create a sample image in memory
    image = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    # Mock the OpenAI API response
    with patch('openai.chat.completions.create') as mock_openai_create:
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content='["t-shirt", "jeans"]'))
        ]
        mock_openai_create.return_value = mock_response

        # Make the request
        files = {'file': ('test.jpg', img_byte_arr, 'image/jpeg')}
        response = client.post("/analyze-image", files=files)

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data['identified_items'] == ["t-shirt", "jeans"]
        assert data['carbon_scores'] == {
            "t-shirt": CARBON_SCORES["t-shirt"],
            "jeans": CARBON_SCORES["jeans"]
        }

def test_analyze_image_no_items():
    # Create a blank image
    image = Image.new('RGB', (100, 100), color='white')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    # Mock the OpenAI API to return an empty list
    with patch('openai.chat.completions.create') as mock_openai_create:
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content='[]'))
        ]
        mock_openai_create.return_value = mock_response

        # Make the request
        files = {'file': ('test.jpg', img_byte_arr, 'image/jpeg')}
        response = client.post("/analyze-image", files=files)

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data['identified_items'] == []
        assert data['carbon_scores'] == {}

def test_analyze_image_invalid_gpt_response():
    # Create a sample image
    image = Image.new('RGB', (100, 100), color='blue')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    # Mock the OpenAI API with an invalid response
    with patch('openai.chat.completions.create') as mock_openai_create:
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content='Invalid response'))
        ]
        mock_openai_create.return_value = mock_response

        # Make the request
        files = {'file': ('test.jpg', img_byte_arr, 'image/jpeg')}
        response = client.post("/analyze-image", files=files)

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data['identified_items'] == []
        assert data['carbon_scores'] == {}

def test_analyze_image_openai_api_error():
    # Create a sample image
    image = Image.new('RGB', (100, 100), color='green')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    # Mock the OpenAI API to raise an exception
    with patch('openai.chat.completions.create') as mock_openai_create:
        mock_openai_create.side_effect = Exception('OpenAI API error')

        # Make the request
        files = {'file': ('test.jpg', img_byte_arr, 'image/jpeg')}
        response = client.post("/analyze-image", files=files)

        # Assertions
        assert response.status_code == 500
        data = response.json()
        assert data['detail'] == 'OpenAI API error'

# Testing /calculate-eco-score endpoint

def test_calculate_eco_score_success():
    payload = {
        "items": ["t-shirt", "jeans", "jacket"]
    }

    response = client.post("/calculate-eco-score", json=payload)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    expected_total_carbon_score = sum(CARBON_SCORES[item.lower()] for item in payload["items"])
    expected_eco_reward_points = calculate_reward_points(expected_total_carbon_score)
    assert data['total_carbon_score'] == expected_total_carbon_score
    assert data['eco_reward_points'] == expected_eco_reward_points

def test_calculate_eco_score_unknown_items():
    payload = {
        "items": ["unknown_item1", "unknown_item2"]
    }

    response = client.post("/calculate-eco-score", json=payload)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data['total_carbon_score'] == 0
    assert data['eco_reward_points'] == 0

def test_calculate_eco_score_empty_items():
    payload = {
        "items": []
    }

    response = client.post("/calculate-eco-score", json=payload)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data['total_carbon_score'] == 0
    assert data['eco_reward_points'] == 0

def test_calculate_eco_score_invalid_payload():
    payload = {
        "invalid_key": ["t-shirt", "jeans"]
    }

    response = client.post("/calculate-eco-score", json=payload)

    # Assertions
    assert response.status_code == 422  # Unprocessable Entity

# Testing /get-offers endpoint

def test_get_offers_success():
    points = 100
    response = client.get(f"/get-offers?points={points}")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    expected_offers = [offer for offer in OFFERS if offer['points_required'] <= points]
    assert data['available_offers'] == expected_offers

def test_get_offers_zero_points():
    points = 0
    response = client.get(f"/get-offers?points={points}")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data['available_offers'] == []

def test_get_offers_negative_points():
    points = -10
    response = client.get(f"/get-offers?points={points}")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data['available_offers'] == []

def test_get_offers_invalid_points():
    response = client.get("/get-offers?points=invalid")

    # Assertions
    assert response.status_code == 422  # Unprocessable Entity
