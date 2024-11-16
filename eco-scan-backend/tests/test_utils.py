# tests/test_utils.py

from utils import calculate_reward_points, parse_gpt_response

def test_calculate_reward_points():
    assert calculate_reward_points(0) == 0
    assert calculate_reward_points(999) == 0
    assert calculate_reward_points(1000) == 1
    assert calculate_reward_points(2500) == 2
    assert calculate_reward_points(5000) == 5

def test_parse_gpt_response_valid():
    response_content = '["t-shirt", "jeans"]'
    items = parse_gpt_response(response_content)
    assert items == ["t-shirt", "jeans"]

def test_parse_gpt_response_empty():
    response_content = '[]'
    items = parse_gpt_response(response_content)
    assert items == []

def test_parse_gpt_response_invalid_json():
    response_content = 'Invalid response'
    items = parse_gpt_response(response_content)
    assert items == []

def test_parse_gpt_response_malformed_json():
    response_content = '["t-shirt", "jeans"'
    items = parse_gpt_response(response_content)
    assert items == []
