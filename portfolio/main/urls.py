from django.urls import path
from .views import HomeView, MiddleEarthProjectView, PortfolioProjectView

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('project-description-middle-earth/', MiddleEarthProjectView.as_view(), name='middle-earth-project-page'),
    path('project-description-portfolio/', PortfolioProjectView.as_view(), name='portfolio-project-page'),
]
