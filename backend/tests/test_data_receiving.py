import typing
import unittest
import unittest.mock as mock

import fastapi.testclient
import parameterized

import application.main
import application.models.place_payload as place_payload


class TestUserInput(unittest.TestCase):
    def test_user_input_positive(self: typing.Self) -> None:
        with mock.patch(
            'db.qdrant_repo.QdrantRepository.search',
            return_value=[
                place_payload.PlacePayload(
                    id=1,
                    title='Танковый музей',
                    description='Танковый музей',
                    score=0.77,
                    latitude=53.12,
                    longitude=13.12,
                ),
            ],
        ):
            client = fastapi.testclient.TestClient(application.main.app)
            data = {
                'prompt': 'Хочу прогуляться рядом с военной техникой',
                'time_for_walk': 5,
                'latitude': 14.88,
                'longitude': 88.41,
            }
            url = '/handle'
            response = client.post(url=url, json=data)
            self.assertEqual(response.status_code, 200)

    @parameterized.parameterized.expand(
        [
            (
                'case1',
                {
                    'prompt': 'Пиво, танчик, танк, балтика',
                    'time_for_walk': 'Google',
                    'latitude': 14.88,
                    'longitude': 88.41,
                },
            ),
            (
                'case2',
                {
                    'prompt': 'Пиво, танчик, танк, балтика',
                    'time_for_walk': 5,
                    'latitude': 'Slots',
                    'longitude': 88.41,
                },
            ),
            (
                'case3',
                {
                    'prompt': 'Танчик' * 100,
                    'time_for_walk': 5,
                    'latitude': 14.88,
                    'longitude': 88.41,
                },
            ),
        ],
    )
    def test_user_input_negative(
        self: typing.Self,
        name: str,
        data: dict,
    ) -> None:
        with mock.patch(
            'db.qdrant_repo.QdrantRepository.search',
            return_value=[
                place_payload.PlacePayload(
                    id=1,
                    title='Танковый музей',
                    description='Танковый музей',
                    score=0.77,
                    latitude=53.12,
                    longitude=13.12,
                ),
            ],
        ):
            client = fastapi.testclient.TestClient(application.main.app)
            url = '/handle'
            response = client.post(url=url, json=data)
            self.assertNotEqual(response.status_code, 200, msg=name)
