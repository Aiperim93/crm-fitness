from django.urls import path, include
from api_v1.views import ClientDetailAPIView, ClientCreateAPIView, CheckAPIView, ClientListAPIView, \
    ActiveClientsInGroupAPIView, TotalActiveClientsAPIView, GroupListAPIView, TrainingCreateAPIView, \
    StaticsView, ClientUpdateAPIView, CoachInfoAPIView, GroupTrainingCreateAPIView, LazyDaysAPIView

from api_v1.views.cache_api_views import AdminView

app_name: str = 'api_v1'

client_urls = [
    path('', ClientListAPIView.as_view(), name='client_list'),
    path('<int:pk>/', ClientDetailAPIView.as_view(), name='client_detail'),
    path('create/', ClientCreateAPIView.as_view(), name='client_create'),
    path('group/<int:group_id>/', ActiveClientsInGroupAPIView.as_view(), name='client_in_group'),
    path('update/<str:telegram_id>/', ClientUpdateAPIView.as_view(), name='client_update'),
    path('check/<str:telegram_id>/', CheckAPIView.as_view(), name='client_check'),
    path('total/active/', TotalActiveClientsAPIView.as_view(), name='total_active_clients'),
]

coach_urls = [
    path('group/<int:group_id>/', CoachInfoAPIView.as_view(), name='coach_info')
]

group_urls = [
    path('', GroupListAPIView.as_view(), name='group_list'),
]

training_urls = [
    path('create/', TrainingCreateAPIView.as_view(), name='training_create'),
]

group_training_urls = [
    path('create/', GroupTrainingCreateAPIView.as_view(), name='group_training_create'),
]

cache_urls = [
    path('cache/', AdminView.as_view(), name='cache'),
]

statistics_urls = [
    path('', StaticsView.as_view(), name='statistics')
]

lazy_days_urls = [
    path('days/<int:pk>/', LazyDaysAPIView.as_view(), name='lazy_days')
]

urlpatterns = [
    path('client/', include(client_urls)),
    path('group/', include(group_urls)),
    path('coach/', include(coach_urls)),
    path('training/', include(training_urls)),
    path('group_training/', include(group_training_urls)),
    path('admin/', include(cache_urls)),
    path('statistics/', include(statistics_urls)),
    path('lazy/', include(lazy_days_urls)),
]
