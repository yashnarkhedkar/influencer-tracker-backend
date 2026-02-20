import uuid

from django.db import models


class Campaign(models.Model):
    class Platform(models.TextChoices):
        YOUTUBE = 'youtube', 'YouTube'
        INSTAGRAM = 'instagram', 'Instagram'
        TIKTOK = 'tiktok', 'TikTok'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        ACTIVE = 'active', 'Active'
        PAUSED = 'paused', 'Paused'
        COMPLETED = 'completed', 'Completed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    platform = models.CharField(max_length=20, choices=Platform.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    budget_total = models.DecimalField(max_digits=10, decimal_places=2)
    budget_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Influencer(models.Model):
    class Platform(models.TextChoices):
        YOUTUBE = 'youtube', 'YouTube'
        INSTAGRAM = 'instagram', 'Instagram'
        TIKTOK = 'tiktok', 'TikTok'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    platform = models.CharField(max_length=20, choices=Platform.choices)
    subscribers = models.BigIntegerField(default=0)
    total_views = models.BigIntegerField(default=0)
    video_count = models.IntegerField(default=0)
    channel_thumbnail = models.URLField(blank=True)
    api_last_fetched = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class CampaignInfluencer(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in-progress', 'In Progress'
        DELIVERED = 'delivered', 'Delivered'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign_influencers')
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE, related_name='campaign_influencers')
    agreed_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deliverables = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.campaign.title} - {self.influencer.name}"
