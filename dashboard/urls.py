from django.urls import path

from dashboard import views

urlpatterns = [
    path('summary/', views.DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('campaigns-by-status/', views.CampaignsByStatusView.as_view(), name='campaigns-by-status'),
    path('budget-overview/', views.BudgetOverviewView.as_view(), name='budget-overview'),
    path('campaigns-over-time/', views.CampaignsOverTimeView.as_view(), name='campaigns-over-time'),
    path('platform-breakdown/', views.PlatformBreakdownView.as_view(), name='platform-breakdown'),
    path('ai-insights/', views.AIInsightsView.as_view(), name='ai-insights'),
]
