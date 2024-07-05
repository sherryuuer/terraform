#!/usr/bin/env python
from cdktf import App, GcsBackend, TerraformStack
from cdktf_cdktf_provider_google.data_google_project import DataGoogleProject
from cdktf_cdktf_provider_google.provider import GoogleProvider

from resources.bigquery import BigqueryDataTransfers
from resources.composers import Composers
from resources.computes import ComputeFirewalls, Computes
from resources.dns import DnsManagedZones, DnsResponsePolicies
from resources.networks import Networks
from resources.routers import ComputeRouters
from resources.storages import StorageBuckets


class MyStack(TerraformStack):

    def __init__(self, scope, name):
        super().__init__(scope, name)

        # 認証に利用する情報
        GoogleProvider(
            self,
            'gcp',
            project='project-name',
            region='asia-northeast1',
            zone='asia-northeast1-a',
        )

        # state管理にGCSを利用する
        # versioningとlifecycleでファイルを保護・世代管理する
        # OKでたら作成＆storages.pyにもリソースを追加
        GcsBackend(
            self,
            bucket='data-engineer-operation-bucket',
            prefix='terraform/state'
        )

        project = DataGoogleProject(
            self,
            'project-name',
            project_id='project-name',
        )

        networks = Networks(self, 'my_project_networks', project)
        Computes(
            self,
            'my_project_computes',
            project,
            networks.vpc,
            networks.common_public_subnet,
            networks.common_private_subnet,
        )
        ComputeFirewalls(self, 'my_project_compute_firewalls',
                         project, networks.vpc)
        ComputeRouters(self, 'my_project', project, networks.vpc)
        Composers(self, 'my_project_composers', networks.vpc,
                  networks.common_private_subnet)
        BigqueryDataTransfers(
            self, 'my_project_bigquery_data_transfers', project)
        StorageBuckets(self, 'my_project_storage_buckets', project)
        DnsManagedZones(self, 'my_project_dns_managed_zones',
                        project, networks.vpc)
        DnsResponsePolicies(
            self, 'my_project_dns_response_policies', project, networks.vpc)


app = App()
MyStack(app, 'test')

app.synth()
