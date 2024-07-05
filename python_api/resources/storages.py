from cdktf_cdktf_provider_google.storage_bucket import StorageBucket
from constructs import Construct


class StorageBuckets(Construct):
    def __init__(self, scope, id, project):
        super().__init__(scope, id)

        StorageBucket(
            self,
            'my_project_data_analysis_bucket',
            force_destroy=False,
            location='ASIA-NORTHEAST1',
            name='my_project-data-analysis-bucket',
            project=project.name,
            public_access_prevention='inherited',
            storage_class='STANDARD',
            uniform_bucket_level_access=True,
        ).import_from('my_project-data-analysis-bucket')

        StorageBucket(
            self,
            'my_project_data_science_bucket',
            force_destroy=False,
            location='ASIA-NORTHEAST1',
            name='my_project-data-science-bucket',
            project=project.name,
            public_access_prevention='inherited',
            storage_class='STANDARD',
            uniform_bucket_level_access=True,
        ).import_from('my_project-data-science-bucket')

        StorageBucket(
            self,
            'my_project_interface_bucket',
            force_destroy=False,
            lifecycle_rule=[{
                'action': {
                    'type': 'Delete'
                },
                'condition': {
                    'age': 8,
                    'with_state': 'ANY'
                }
            }],
            location='ASIA-NORTHEAST1',
            name='my_project-interface-bucket',
            project=project.name,
            public_access_prevention='inherited',
            storage_class='STANDARD',
            uniform_bucket_level_access=True,
        ).import_from('my_project-interface-bucket')

        StorageBucket(
            self,
            'my_project_snapshot_archive_bucket',
            force_destroy=False,
            location='ASIA-NORTHEAST1',
            name='my_project-snapshot-archive-bucket',
            project=project.name,
            public_access_prevention='enforced',
            storage_class='ARCHIVE',
            uniform_bucket_level_access=True,
        ).import_from('my_project-snapshot-archive-bucket')

        StorageBucket(
            self,
            'my_project_test_bucket',
            force_destroy=False,
            location='ASIA-NORTHEAST1',
            name='my_project-test-bucket',
            project=project.name,
            public_access_prevention='enforced',
            storage_class='STANDARD',
            uniform_bucket_level_access=True,
        ).import_from('my_project-test-bucket')

        StorageBucket(
            self,
            'asiaartifactsmy_projectappspotcom',
            force_destroy=False,
            location='ASIA',
            name='asia.artifacts.my_project.appspot.com',
            project=project.name,
            public_access_prevention='inherited',
            storage_class='STANDARD',
            uniform_bucket_level_access=True,
        ).import_from('asia.artifacts.my_project.appspot.com')
