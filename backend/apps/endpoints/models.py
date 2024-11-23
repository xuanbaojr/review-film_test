from django.db import models

# Create your models here
class Endpoint(models.Model):

    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

class MLAlgorithm(models.Model):

    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    code = models.TextField(max_length=1000)
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)

class MLAlgorithmStatus(models.Model):

    status = models.CharField(max_length=128)
    active = models.BooleanField()
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name = "status")

class MLRequests(models.Model):

    input_data = models.TextField(max_length=10000)
    full_response = models.TextField(max_length=10000)
    response = models.TextField(max_length=10000)
    feedback = models.TextField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)


##########################
class Movie(models.Model):
    genres = models.TextField(max_length=1000)
    genres = models.TextField(max_length=1000)
    director = models.CharField(max_length=256)
    cast = models.TextField(max_length=1000)
    keywords = models.TextField(max_length=1000)