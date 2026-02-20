from django.urls import path

from ai_tools import views

urlpatterns = [
    path('generate-brief/', views.GenerateBriefView.as_view(), name='generate-brief'),
    path('suggest-titles-hashtags/', views.SuggestTitlesHashtagsView.as_view(), name='suggest-titles-hashtags'),
]
