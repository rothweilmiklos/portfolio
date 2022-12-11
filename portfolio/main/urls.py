from django.urls import path
from .views import HomeView, MiddleEarthProjectView

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('', MiddleEarthProjectView.as_view(), name='middle-earth-project-page'),
    path('', HomeView.as_view(), name='portfolio-project-page'),
]
