import enum
import functools
import typing

import torch
import torch.nn.functional as f
import transformers


class _TextGenerationModel:
    type_model: str = 'text-generation'
    name_model: str = 'Qwen/Qwen3-0.6B'

    def __init__(self: typing.Self) -> None:
        self._model: transformers.TextGenerationPipeline = transformers.pipeline(
            self.type_model,
            self.name_model,
        )

    def __call__(self: typing.Self, prompt: str) -> None:
        messages = [
            {'role': 'user', 'content': prompt},
        ]
        text_answer: str = self._model(messages)[0]['generated_text'][1]['content']
        return text_answer.split('</think>')[-1].strip()


text_generation_model = _TextGenerationModel()


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
        self._tokenizer = transformers.AutoTokenizer.from_pretrained(self.name_model)
        self._model = transformers.T5EncoderModel.from_pretrained(self.name_model)

    def multi_call(self: typing.Self, texts: list[str]) -> list[list[float]]:
        return [self(el) for el in texts]

    @functools.lru_cache
    def __call__(self: typing.Self, text: str) -> list[float]:
        texts = [f'{_Prefix.SEARCH_QUERY.value}:{text}']
        tokenized_inputs = self._tokenizer(
            texts,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors='pt',
        )
        with torch.no_grad():
            outputs = self._model(**tokenized_inputs)

        embeddings = outputs.last_hidden_state[:, 0]
        embeddings = f.normalize(embeddings, p=2, dim=1)
        return embeddings.tolist()[0]


embedding_model = _EmbeddingModel()
