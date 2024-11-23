from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException


from apps.endpoints.models import *
from apps.endpoints.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics


import transaction


# Authentication

# Create your views here.
def deactive_other_statuses(instance):
    old_statuses = MLAlgorithmStatus.objects.filter(
        parent_dl_comment = instance.parent_dl_comment,
        created_at__lt = instance.created_at,
        active = True
    )
    for old_status in old_statuses:
        old_status.active = False
    MLAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])

class EndpointViewSet(mixins.RetrieveModelMixin, 
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()

class MLAlgorithmViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithm.objects.all()


def deactivate_other_statuses(instance):
    old_statuses = MLAlgorithmStatus.objects.filter(parent_mlalgorithm = instance.parent_mlalgorithm,
                                                        created_at__lt=instance.created_at,
                                                        active=True)
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    MLAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])

class MLAlgorithmStatusViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    serializer_class = MLAlgorithmStatusSerializer
    queryset = MLAlgorithmStatus.objects.all()
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                # set active=False for other statuses
                deactivate_other_statuses(instance)



        except Exception as e:
            raise APIException(str(e))

class MLRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin
):
    serializer_class = MLRequestSerializer
    queryset = MLRequests.objects.all()


import json
import numpy as np
from rest_framework import views, status
from rest_framework.response import Response
from apps.dl.registry import MLRegistry
from backend.wsgi import registry

class PredictView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request, endpoint_name, format=None):
        algorithm_status = self.request.query_params.get("status", "production")
        algorithm_version = self.request.query_params.get("version")

        algs = MLAlgorithm.objects.filter(parent_endpoint__name=endpoint_name,
                                          status__status=algorithm_status,
                                          status__active=True)
        if algorithm_version is not None:
            algs = algs.filter(version=algorithm_version)
            print('algs', algs)
        
        if len(algs) == 0:
            return Response(
                {"status": "Error", "message":"ML Algorithm is not available"},
                status = status.HTTP_400_BAD_REQUEST
            )

        if len(algs) !=1 and algorithm_status != 'ab_testing':
            return Response(
                {"status":"Error", "message":"ML algorithm selection is ambiguous. Please specify algorithm version"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        alg_index = 0
        if algorithm_status == "ab_testing":
            alg_index = 0 if np.random.rand() < 0.5 else 1
        
        algorithm_object = registry.endpoints[algs[alg_index].id]
        prediction = algorithm_object.predict("The Godfather")

        # ml_request = MLRequests(
        #     input_data=json.dumps(request.data),
        #     full_response=prediction,
        #     feedback="ok",
        #     parent_mlalgorithm=algs[alg_index]
        # )
        # ml_request.save()

        return Response(prediction)