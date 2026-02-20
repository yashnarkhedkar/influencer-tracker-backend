from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from campaigns.models import Campaign, CampaignInfluencer, Influencer
from campaigns.serializers import (
    CampaignInfluencerSerializer,
    CampaignSerializer,
    InfluencerSerializer,
)
from campaigns.services.youtube import fetch_channel_stats


class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer

    def get_queryset(self):
        queryset = Campaign.objects.all().order_by('-created_at')
        status_param = self.request.query_params.get('status')
        platform_param = self.request.query_params.get('platform')
        if status_param:
            queryset = queryset.filter(status=status_param)
        if platform_param:
            queryset = queryset.filter(platform=platform_param)
        return queryset


class InfluencerViewSet(viewsets.ModelViewSet):
    serializer_class = InfluencerSerializer
    queryset = Influencer.objects.all().order_by('-created_at')

    @action(detail=True, methods=['post'])
    def refresh_stats(self, request, pk=None):
        influencer = self.get_object()
        stats = fetch_channel_stats(influencer.handle)
        if not stats:
            return Response(
                {'detail': 'Unable to fetch channel stats.'},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        influencer.subscribers = stats['subscribers']
        influencer.total_views = stats['total_views']
        influencer.video_count = stats['video_count']
        influencer.channel_thumbnail = stats['channel_thumbnail']
        influencer.api_last_fetched = timezone.now()
        influencer.save(update_fields=[
            'subscribers',
            'total_views',
            'video_count',
            'channel_thumbnail',
            'api_last_fetched',
        ])
        serializer = self.get_serializer(influencer)
        return Response(serializer.data)


class CampaignInfluencerViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignInfluencerSerializer

    def get_queryset(self):
        queryset = CampaignInfluencer.objects.select_related('campaign', 'influencer')
        campaign_id = self.request.query_params.get('campaign')
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        return queryset.order_by('-created_at')
