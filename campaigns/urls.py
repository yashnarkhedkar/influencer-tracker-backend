from rest_framework.routers import DefaultRouter

from campaigns.views import CampaignInfluencerViewSet, CampaignViewSet, InfluencerViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'influencers', InfluencerViewSet, basename='influencer')
router.register(r'campaign-influencers', CampaignInfluencerViewSet, basename='campaign-influencer')

urlpatterns = router.urls
