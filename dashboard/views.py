from datetime import date, timedelta
import hashlib
import json
from pathlib import Path

from django.db.models import Avg, Count, F, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from campaigns.models import Campaign, Influencer
from dashboard.ai import generate_insights


_REQUEST_CACHE_FILENAME = "ai_request_cache.json"
_REQUEST_CACHE_LIMIT = 10


def _request_cache_path() -> Path:
    return Path(__file__).resolve().parents[1] / _REQUEST_CACHE_FILENAME


def _load_request_cache() -> dict:
    path = _request_cache_path()
    if not path.exists():
        return {"order": [], "items": {}}
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if (
            isinstance(data, dict)
            and isinstance(data.get("order"), list)
            and isinstance(data.get("items"), dict)
        ):
            return data
    except Exception:
        return {"order": [], "items": {}}
    return {"order": [], "items": {}}


def _save_request_cache(cache: dict) -> None:
    path = _request_cache_path()
    with path.open("w", encoding="utf-8") as handle:
        json.dump(cache, handle, indent=2)


def _request_cache_key(payload: dict) -> str:
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _summary_payload():
    totals = Campaign.objects.aggregate(
        total_campaigns=Count('id'),
        total_budget=Sum('budget_total'),
        total_spent=Sum('budget_spent'),
    )
    active_campaigns = Campaign.objects.filter(status=Campaign.Status.ACTIVE).count()
    total_influencers = Influencer.objects.count()

    avg_duration = Campaign.objects.annotate(
        duration=F('end_date') - F('start_date')
    ).aggregate(avg_duration=Avg('duration'))['avg_duration']

    avg_days = avg_duration.days if avg_duration else 0

    return {
        'total_campaigns': int(totals['total_campaigns'] or 0),
        'active_campaigns': int(active_campaigns),
        'total_budget': float(totals['total_budget'] or 0),
        'total_spent': float(totals['total_spent'] or 0),
        'total_influencers': int(total_influencers),
        'avg_campaign_duration_days': int(avg_days),
    }


class DashboardSummaryView(APIView):
    def get(self, request):
        return Response(_summary_payload())


class CampaignsByStatusView(APIView):
    def get(self, request):
        data = (
            Campaign.objects.values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )
        return Response(list(data))


class BudgetOverviewView(APIView):
    def get(self, request):
        data = (
            Campaign.objects.order_by('-budget_total')
            .values('title', 'budget_total', 'budget_spent')[:8]
        )
        return Response([
            {
                'title': item['title'],
                'budget_total': float(item['budget_total']),
                'budget_spent': float(item['budget_spent']),
            }
            for item in data
        ])


class CampaignsOverTimeView(APIView):
    def get(self, request):
        today = timezone.now().date()
        start_month = date(today.year, today.month, 1)
        a_year_ago = start_month
        for _ in range(11):
            a_year_ago = (a_year_ago - timedelta(days=1)).replace(day=1)

        data = (
            Campaign.objects.filter(created_at__date__gte=a_year_ago)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        payload = [
            {
                'month': item['month'].strftime('%b %Y'),
                'count': item['count'],
            }
            for item in data
        ]
        return Response(payload)


class PlatformBreakdownView(APIView):
    def get(self, request):
        data = (
            Campaign.objects.values('platform')
            .annotate(count=Count('id'))
            .order_by('platform')
        )
        return Response(list(data))


class AIInsightsView(APIView):
    def get(self, request):
        summary = _summary_payload()
        campaigns_by_status = list(
            Campaign.objects.values('status').annotate(count=Count('id'))
        )
        platform_breakdown = list(
            Campaign.objects.values('platform').annotate(count=Count('id'))
        )
        data = {
            'summary': summary,
            'campaigns_by_status': campaigns_by_status,
            'platform_breakdown': platform_breakdown,
        }
        cache = _load_request_cache()
        cache_key = _request_cache_key(data)
        cached_item = cache.get("items", {}).get(cache_key)
        if isinstance(cached_item, str) and cached_item:
            return Response({'insights': cached_item})

        insights_text = generate_insights(data)
        if insights_text:
            order = cache.get("order", [])
            items = cache.get("items", {})
            if cache_key not in items:
                order.append(cache_key)
            items[cache_key] = insights_text
            while len(order) > _REQUEST_CACHE_LIMIT:
                oldest = order.pop(0)
                items.pop(oldest, None)
            cache["order"] = order
            cache["items"] = items
            _save_request_cache(cache)
        return Response({'insights': insights_text})
