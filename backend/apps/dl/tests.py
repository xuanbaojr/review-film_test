from django.test import TestCase
import inspect
from apps.dl.registry import DLRegistry
from apps.dl.comment.comment_predict import Comment

class DLTests(TestCase):
    def test_comment(self):
        comment = "This film is very good!"
        predictor = Comment()
        result = predictor.predict(comment)
        print("result", result)
    
    def test_registry(self):
        registry = DLRegistry()
        endpoint_name = "income_classifier"
        algorithm_object = Comment()
        algorithm_name = "comment LSTM"
        algorithm_status = "production"
        algorithm_version = "0.0.1"
        algorithm_owner = "XuanBao01"
        algorithm_description = "This is comment sentiment analysis by LSTM"
        algorithm_code = inspect.getsource(Comment)
        print("algorithm_code:", algorithm_code)

        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name, algorithm_status,
                               algorithm_version, algorithm_owner, algorithm_description,
                               algorithm_code)