from cdktf_cdktf_provider_google.compute_router import ComputeRouter
from constructs import Construct


class ComputeRouters(Construct):
    def __init__(self, scope, id, project, vpc):
        super().__init__(scope, id)

        ComputeRouter(
            self,
            'my_project_rtr_001',
            name='my_project-rtr-001',
            network=vpc.id,
            project=project.name,
            region='asia-northeast1'
        ).import_from('my_project-rtr-001')
