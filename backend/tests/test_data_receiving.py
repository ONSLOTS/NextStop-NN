import pathlib
import pickle

# """Tests of receiving data from frontend."""

# import unittest

# import fastapi.testclient
# import parameterized

# import application.main


# class TestUserInput(unittest.TestCase):
#     """Tests of receiving data from frontend."""

#     def test_user_input_positive(self) -> None:
#         """Test of receiving json on /handle."""
#         client = fastapi.testclient.TestClient(application.main.app)
#         data = {
#             'prompt': 'Пиво, танчик, танк, балтика',
#             'time_for_walk': 5,
#             'latitude': 14.88,
#             'longitude': 88.41,
#         }
#         url = '/handle'
#         response = client.post(url=url, json=data)

#         self.assertEqual(response.status_code, 200)

#     @parameterized.parameterized.expand(
#         [
#             (
#                 'case1',
#                 {
#                     'prompt': 'Пиво, танчик, танк, балтика',
#                     'time_for_walk': 'Gool',
#                     'latitude': 14.88,
#                     'longitude': 88.41,
#                 },
#             ),
#             (
#                 'case2',
#                 {
#                     'prompt': 'Пиво, танчик, танк, балтика',
#                     'time_for_walk': 5,
#                     'latitude': 'Slots',
#                     'longitude': 88.41,
#                 },
#             ),
#             (
#                 'case3',
#                 {
#                     'prompt': 'Танчик' * 100,
#                     'time_for_walk': 5,
#                     'latitude': 14.88,
#                     'longitude': 88.41,
#                 },
#             ),
#         ],
#     )
#     def test_user_input_negative(self, name: str, data: dict) -> None:
#         """Test unvalid json on /handle."""
#         client = fastapi.testclient.TestClient(application.main.app)
#         url = '/handle'
#         response = client.post(url=url, json=data)
#         self.assertNotEqual(response.status_code, 200, msg=name)
file_path = pathlib.Path(__file__).parent.parent / 'open_street_map.pkl'
try:
    with open(file_path, 'rb') as f:
        reachability_matrix = pickle.load(f)
        print(len(reachability_matrix))
except FileNotFoundError:
    print('File not found')
except pickle.UnpicklingError:
    print('Error while attempting to load pkl file')
