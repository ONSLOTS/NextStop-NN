import enum
import functools
import typing

import torch
import torch.nn.functional as f
import transformers

from models import place_payload


class _TextGenerationModel:
    type_model: str = 'text-generation'
    name_model: str = 'Qwen/Qwen3-0.6B'

    def __init__(self: typing.Self) -> None:
        self._tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.name_model,
            dtype='auto',
            device_map='auto',
        )
        self._model = transformers.AutoModelForCausalLM.from_pretrained(
            self.name_model,
            dtype='auto',
            device_map='auto',
        )

    def get_desc_selection(
        self: typing.Self,
        prompt: str,
        places: list[place_payload.PlacePayload],
    ) -> list[str]:
        ans: list[str] = []
        for place in places:
            local_prompt: str = (
                f'Пиши максимально коротоко. '
                f'Напиши почему выбранное место ({place.title}) подходит запросу пользователя, обращаясь к нему на вы. '
                f'Запрос пользователя: {prompt}. '
                f'В ответе используй факты из описания выбранного места: {place.description}. '
                'Формат: обращайтесь на «Вы», в тексте используйте фразы "Для Вашего запроса" или'
                ' "Исходя из Ваших предпочтений".'
            )

            ans.append(self(local_prompt))

        return ans

    def __call__(self: typing.Self, prompt: str) -> str:
        messages = [
            {'role': 'user', 'content': prompt},
        ]
        text = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        model_inputs = self._tokenizer([text], return_tensors='pt').to(
            self._model.device,
        )
        generated_ids = self._model.generate(
            **model_inputs,
            max_new_tokens=32768,
        )
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]) :].tolist()
        try:
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0

        return self._tokenizer.decode(
            output_ids[index:],
            skip_special_tokens=True,
        ).strip('\n')


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
