from django.urls import path
from .views.models import *
from .views.movies import *
urlpatterns = [
    path("endpoints", EndpointViewSet.as_view({'get':'list'}) ),
    path("mlalgorithms", MLAlgorithmViewSet.as_view({'get':'list'})),
    path("mlrequests", MLRequestViewSet.as_view({'get':'list'})),
    path('<str:endpoint_name>/predict', PredictView.as_view()),

    path('getmoviebyid/<str:movie_id>', GetMovieByIdView.as_view())
]

