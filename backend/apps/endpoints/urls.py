from django.urls import path
from .views.models import *
urlpatterns = [
    path("endpoints", EndpointViewSet.as_view({'get':'list'}) ),
    path("dlcomment", DLCommentViewSet.as_view({'get':'list'})),
    path("dlcommentstatus", DLCommentStatusViewSet.as_view({'get':'list'})),
    path("dlcommentrequests", DLCommentRequestViewSet.as_view({'get':'list'})),
    path('<str:endpoint_name>/predict', PredictView.as_view())
]

