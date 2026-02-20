from decouple import config
from googleapiclient.discovery import build


def fetch_channel_stats(channel_id: str):
    api_key = config('YOUTUBE_API_KEY', default=None)
    if not api_key:
        return None
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = (
            youtube.channels()
            .list(part='statistics,snippet', id=channel_id)
            .execute()
        )
        items = response.get('items', [])
        if not items:
            return None
        channel = items[0]
        stats = channel.get('statistics', {})
        snippet = channel.get('snippet', {})
        thumbnails = snippet.get('thumbnails', {})
        thumbnail = (
            thumbnails.get('high', {})
            or thumbnails.get('medium', {})
            or thumbnails.get('default', {})
        )
        return {
            'subscribers': int(stats.get('subscriberCount', 0)),
            'total_views': int(stats.get('viewCount', 0)),
            'video_count': int(stats.get('videoCount', 0)),
            'channel_thumbnail': thumbnail.get('url', ''),
        }
    except Exception:
        return None
