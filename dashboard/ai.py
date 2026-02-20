import json

from ai_tools.openai_client import get_openai_client


def generate_insights(data: dict) -> str:
    client = get_openai_client()
    if not client:
        return 'OpenAI API key not configured.'

    system_prompt = (
        'You are a data analyst for influencer marketing campaigns. '
        'Provide exactly 3 concise, actionable bullet points.'
    )
    user_prompt = (
        'Here is the latest dashboard data in JSON:\n'
        f"{json.dumps(data, indent=2)}\n\n"
        'Return three bullet points prefixed with "•".'
    )

    try:
        response = client.responses.create(
            model='gpt-4o',
            input=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
        )
        return (response.output_text or '').strip()
    except Exception:
        return 'Unable to generate insights at this time.'
