from cdktf_cdktf_provider_google.bigquery_data_transfer_config import (
    BigqueryDataTransferConfig,
)
from constructs import Construct


class BigqueryDataTransfers(Construct):
    def __init__(self, scope, id, project):
        super().__init__(scope, id)

        # BQ transfer
        BigqueryDataTransferConfig(
            self,
            'my_project_copy_of_de_choice_cms_mart',
            data_refresh_window_days=0,
            data_source_id='cross_region_copy',
            destination_dataset_id='prod_choice_cms_mart',
            disabled=False,
            display_name='Copy of dev_choice_cms_mart',
            location='asia-northeast1',
            params={
                'overwrite_destination_table': 'true',
                'source_dataset_id': 'dev_choice_cms_mart',
                'source_project_id': 'my_project',
            },
            project=project.name,
            schedule='every 24 hours',
            schedule_options={
                'disable_auto_scheduling': False,
                'end_time': None,
                'start_time': '2023-03-20T23:00:00Z',
            },
        ).import_from('projects/978277524466/locations/asia-northeast1/transferConfigs/640889c6-0000-25c5-8ac4-240588713cc4')

        BigqueryDataTransferConfig(
            self,
            'my_project_google_ads_bqdatatransfer_converted',
            data_refresh_window_days=0,
            data_source_id='google_ads',
            destination_dataset_id='google_ads',
            disabled=False,
            display_name='my_project-google-ads-bqdatatransfer_converted',
            email_preferences={
                'enable_failure_email': True,
            },
            location='asia-northeast1',
            params={
                'compatible_report_date': '2023-03-28',
                'create_adwords_compatible_view_from': '63371851-0000-2e3a-9ee5-94eb2c0e8f66',
                'customer_id': '117-382-0148',
            },
            project='my_project',
            schedule='every day 15:00',
            schedule_options={
                'disable_auto_scheduling': False,
                'end_time': None,
                'start_time': '2023-03-28T15:00:00Z',
            },
        ).import_from('projects/978277524466/locations/asia-northeast1/transferConfigs/64227c4d-0000-2d8f-9e0b-001a114fea70')
