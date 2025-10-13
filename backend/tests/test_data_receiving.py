"""Tests of receiving data from frontend."""
import pathlib
import sys
import unittest

import fastapi.testclient
import parameterized

project_root = pathlib.Path(__file__).parent.parent / 'application'
sys.path.append(str(project_root))
import application.main


class TestUserInput(unittest.TestCase):
    """Tests of receiving data from frontend."""

    def test_user_input_positive(self) -> None:
        """Test of receiving json on /handle."""
        client = fastapi.testclient.TestClient(application.main.app)
        data = {
            'prompt': 'Пиво, танчик, танк, балтика',
            'time_for_walk': 5,
            'latitude': 14.88,
            'longitude': 88.41,
        }
        url = '/handle'
        response = client.post(url=url, json=data)

        self.assertEqual(response.status_code, 200)
        for key in data:
            self.assertIn(key, response.json().keys())

    @parameterized.parameterized.expand([
        ('case1', {
            'prompt': 'Пиво, танчик, танк, балтика',
            'time_for_walk': 'Gool',
            'latitude': 14.88,
            'longitude': 88.41,
            }),
        ('case2', {
            'prompt': 'Пиво, танчик, танк, балтика',
            'time_for_walk': 5,
            'latitude': 'Slots',
            'longitude': 88.41,
        }),
        ('case3', {
            'prompt': 'Танчик' * 100,
            'time_for_walk': 5,
            'latitude': 14.88,
            'longitude': 88.41,
        }),
    ])
    def test_user_input_negative(self, name: str, data: dict) -> None:
        """Test unvalid json on /handle."""
        client = fastapi.testclient.TestClient(application.main.app)
        url = '/handle'
        response = client.post(url=url, json=data)
        self.assertNotEqual(
            response.status_code,
            200,
            msg=name)
