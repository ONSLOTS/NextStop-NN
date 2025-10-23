import typing
import unittest

import application.models.place_payload as place_payload
import application.services.utils as utils

PLACES: typing.Final[list[place_payload.PlacePayload]] = [
    place_payload.PlacePayload(
            id=1,
            title='Танковый музей',
            description='Танковый музей',
            score=0.77,
            latitude=53.12,
            longitude=13.12,
    ),
]


class TestGetBestRoute(unittest.TestCase):
    def test_zero_places_positive(self: typing.Self) -> None:
        result = utils.get_best_route(
            [],
            24,
        )
        self.assertIs(result, None)

    def test_one_places_positive(self: typing.Self) -> None:
        result = utils.get_best_route(
            PLACES,
            24,
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], place_payload.PlacePayload)
