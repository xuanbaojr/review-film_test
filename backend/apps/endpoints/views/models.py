from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException


from apps.endpoints.models import *
from apps.endpoints.serializers import *

import transaction


# Authentication

# Create your views here.
def deactive_other_statuses(instance):
    old_statuses = DL_CommentStatus.objects.filter(
        parent_dl_comment = instance.parent_dl_comment,
        created_at__lt = instance.created_at,
        active = True
    )
    for old_status in old_statuses:
        old_status.active = False
    DL_CommentStatus.objects.bulk_update(old_statuses, ["active"])

class EndpointViewSet(mixins.RetrieveModelMixin, 
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()

class DLCommentViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = DL_CommentSerializer
    queryset = DL_Comment.objects.all()

class DLCommentStatusViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = DL_CommentStatusSerializer
    queryset = DL_CommentStatus.objects.all()
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                deactive_other_statuses(instance)
        except Exception as e:
            raise APIException(str(e))

class DLCommentRequestViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                              viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = DL_CommentRequestSerializer
    queryset = DL_CommentRequest.objects.all()



import json
import numpy as np
from rest_framework import views, status
from rest_framework.response import Response
from apps.dl.registry import DLRegistry
from backend.wsgi import registry

class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):
        algorithm_status = self.request.query_params.get("status", "production")
        algorithm_version = self.request.query_params.get("version")

        algs = DL_Comment.objects.filter(parent_endpoint__name=endpoint_name, status__status=algorithm_status,
                                         status__active=True)
        if algorithm_version is not None:
            algs.filter(version=algorithm_version)
        
        if len(algs) == 0:
            return Response(
                {"status": "Error", "message": "ML algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(algs) != 1 and algorithm_status != "ab_testing":
            return Response(
                {"status": "Error", "message": "ML algorithm selection is ambiguous. Please specify algorithm version."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        alg_index = 0
        if algorithm_status == "ab_testing":
            alg_index = 0 if np.random.rand() < 0.5 else 1
        
        algorithm_object = registry.endpoints[algs[alg_index].id]
        prediction = algorithm_object.predict(request.data)
        print('prediction:', prediction)

        label = prediction
        dl_request = DL_CommentRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            parent_dl_comment=algs[alg_index],
        )
        dl_request.save()

        return Response(prediction)