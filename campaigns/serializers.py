from rest_framework import serializers

from campaigns.models import Campaign, CampaignInfluencer, Influencer


class InfluencerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Influencer
        fields = '__all__'


class CampaignInfluencerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignInfluencer
        fields = '__all__'


class CampaignInfluencerReadSerializer(serializers.ModelSerializer):
    influencer = InfluencerSerializer(read_only=True)

    class Meta:
        model = CampaignInfluencer
        fields = '__all__'


class CampaignSerializer(serializers.ModelSerializer):
    campaign_influencers = CampaignInfluencerReadSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = '__all__'
