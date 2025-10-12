import enum
import functools
import typing

import sentence_transformers
import torch


class _Prefix(enum.Enum):
    SEARCH_QUERY = 'search_query'
    PARAPHRASE = 'paraphrase'
    CATEGORIZE = 'categorize'
    CATEGORIZE_SENTIMENT = 'categorize_sentiment'
    CATEGORIZE_TOPIC = 'categorize_topic'
    CATEGORIZE_ENTAILMENT = 'categorize_entailment'


EMBEDDING_LENGTH: typing.Final[int] = 1536


class _EmbeddingModel:
    name_model: str = 'ai-forever/FRIDA'

    def __init__(self: typing.Self) -> None:
        self._model = sentence_transformers.SentenceTransformer(
            self.name_model,
            device='cuda' if torch.cuda.is_available() else 'cpu',
            cache_folder='./model_cache',
        )

    def multi_call(self: typing.Self, texts: list[str]) -> list[list[float]]:
        return self._model.encode(
            texts,
            prompt_name=_Prefix.SEARCH_QUERY.value,
        ).tolist()

    @functools.lru_cache
    def __call__(self: typing.Self, text: str) -> list[float]:
        return self._model.encode(
            text,
            prompt_name=_Prefix.SEARCH_QUERY.value,
        ).tolist()


embedding_model = _EmbeddingModel()
