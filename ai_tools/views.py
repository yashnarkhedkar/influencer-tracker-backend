import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_tools.openai_client import get_openai_client


def _extract_json(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find('{')
        end = text.rfind('}')
        if start == -1 or end == -1 or end <= start:
            return None
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return None


class GenerateBriefView(APIView):
    def post(self, request):
        payload = request.data
        client = get_openai_client()
        if not client:
            return Response({'detail': 'OpenAI API key not configured.'}, status=500)

        system_prompt = (
            'You are an expert influencer marketing strategist. '
            'Generate a complete campaign brief.'
        )
        user_prompt = (
            f"Product Name: {payload.get('product_name')}\n"
            f"Target Audience: {payload.get('target_audience')}\n"
            f"Platform: {payload.get('platform')}\n"
            f"Tone: {payload.get('tone')}\n"
            f"Budget: {payload.get('budget')}\n\n"
            'Include: Campaign Goal, Content Guidelines, Dos & Don\'ts, '
            'Deliverables, KPIs, and Suggested Hashtags. '
            'Return text content starting with "## Campaign Brief".'
        )

        try:
            response = client.responses.create(
                model='gpt-4o-mini',
                input=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt},
                ],
            )
            brief = (response.output_text or '').strip()
        except Exception as e:
            print("OpenAI error:", str(e))  # print actual error
            return Response({"detail": str(e)}, status=502)

        return Response({'brief': brief})


class SuggestTitlesHashtagsView(APIView):
    def post(self, request):
        payload = request.data
        client = get_openai_client()
        if not client:
            return Response({'detail': 'OpenAI API key not configured.'}, status=500)

        system_prompt = (
            'You are a creative marketing assistant. '
            'Return ONLY valid JSON with keys "titles" and "hashtags".'
        )
        user_prompt = (
            f"Description: {payload.get('description')}\n"
            f"Platform: {payload.get('platform')}\n\n"
            'Provide 5 campaign title suggestions in the "titles" array and '
            '10 relevant hashtags in the "hashtags" array. '
            'Return JSON only, no markdown.'
        )

        try:
            response = client.responses.create(
                model='gpt-4o',
                input=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt},
                ],
            )
            text = (response.output_text or '').strip()
            data = _extract_json(text)
            if not data or 'titles' not in data or 'hashtags' not in data:
                raise ValueError('Invalid JSON structure')
        except Exception:
            return Response({'detail': 'OpenAI request failed.'}, status=502)

        return Response({'titles': data['titles'], 'hashtags': data['hashtags']})
