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
from apps.dl.registry import DLRegistry
from apps.dl.comment.comment_predict import Comment

try:
    registry = DLRegistry()
    predictor = Comment()
    registry.add_algorithm(endpoint_name="income_classifier",
                           algorithm_object=predictor,
                           algorithm_name='comment LSTM',
                           algorithm_status="production",
                           algorithm_version="0.0.1",
                           owner="XuanBao01",
                           algorithm_description="This is sentiment model!",
                           algorithm_code=inspect.getsource(Comment))
except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))