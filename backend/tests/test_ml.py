import typing
import unittest

import parametrize

import ml

TESTS_FOR_TEST: list[str] = [
    'B Ярославской области разрешили работу бань, но без посетителей',
    'Женщину доставили в больницу, за ee жизнь сейчас борются врачи.',
    'Сколько программистов нужно, чтобы вкрутить лампочку?',
    'Ярославским баням разрешили работать без посетителей',
    'Женщину спасают врачи.',
    'Чтобы вкрутить лампочку, требуется три программиста: '
    'один напишет программу извлечения лампочки, другой — вкручивания лампочки, '
    'a третий проведет тестирование.',
]
PROMPT_FOR_TEST = 'Что ты за модель?'


class TestTextGenerationModel(unittest.TestCase):
    def test_call(self: typing.Self) -> None:
        ans: str = ml.text_generation_model(PROMPT_FOR_TEST)
        self.assertIsInstance(ans, str)


class TestEmbeddingModel(unittest.TestCase):
    @parametrize.parametrize('text', TESTS_FOR_TEST)
    def test_call(self: typing.Self, text: str) -> None:
        embedding = ml.embedding_model(text)
        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), ml.EMBEDDING_LENGTH)
        self.assertIsInstance(embedding[0], float)

    def test_equivalences(self: typing.Self) -> None:
        ans1: list = []
        for el in TESTS_FOR_TEST:
            embedidng = ml.embedding_model(el)
            ans1.append(embedidng)

        ans2 = ml.embedding_model.multi_call(TESTS_FOR_TEST)
        self.assertEqual(ans1, ans2)
