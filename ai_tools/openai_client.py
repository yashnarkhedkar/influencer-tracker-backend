from decouple import config
from openai import OpenAI


def get_openai_client():
    api_key = config('OPENAI_API_KEY', default=None)
    if not api_key:
        return None
    return OpenAI(api_key=api_key)
