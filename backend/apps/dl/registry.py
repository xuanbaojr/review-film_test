from apps.endpoints.models import *

class DLRegistry:
    def __init__(self) -> None:
        self.endpoints = {}
    
    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name,
                      algorithm_status, algorithm_version, owner,
                      algorithm_description, algorithm_code):
        
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name, owner=owner)

        database_object, algorithm_created = DL_Comment.objects.get_or_create(
            name=algorithm_name,
            description=algorithm_description,
            code=algorithm_code,
            version=algorithm_version,
            owner=owner,
            parent_endpoint=endpoint
        )

        if algorithm_created:
            status = DL_CommentStatus(status=algorithm_status,
                                      created_by=owner,
                                      parent_dl_comment=database_object,
                                      active=True)
            status.save()
        
        self.endpoints[database_object.id] = algorithm_object