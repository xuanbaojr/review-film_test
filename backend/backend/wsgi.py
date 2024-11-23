"""
WSGI config for server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()


# DL Registry
import inspect
from apps.dl.registry import MLRegistry
from apps.dl.comment.comment_predict import Comment
from apps.dl.recommend.knn import KNN

try:
    registry = MLRegistry()
    comment = Comment()
    registry.add_algorithm(endpoint_name="comment",
                           algorithm_object=comment,
                           algorithm_name='naive_bayes',
                           algorithm_status="production",
                           algorithm_version="0.0.1",
                           owner="XuanBao01",
                           algorithm_description="This is sentiment model!",
                           algorithm_code=inspect.getsource(Comment))
    
    knn_v1 = KNN()
    registry.add_algorithm(endpoint_name="recommendation",
                           algorithm_object=knn_v1,
                           algorithm_name="knn",
                           algorithm_status="production",
                           algorithm_version="v1",
                           owner="XuanBao01",
                           algorithm_description="knn model for film recommendation system",
                           algorithm_code=inspect.getsource(knn_v1))
    
    # knn_v2 = KNN(x=1)
    
except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))