from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import *
from django.views import View

import pandas as pd
class GetMovieByIdView(View):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):

        movie_id = kwargs['movie_id']
        movie = get_object_or_404(Movie, original_title=movie_id)

        data = {
            "id": movie_id,
            "original_title": movie.original_title,
            "genres": movie.genres,
            "director": movie.director,
            "casts": movie.cast,
            "keywords": movie.keywords
        }
        return JsonResponse(data)