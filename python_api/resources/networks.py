from cdktf_cdktf_provider_google.compute_network import ComputeNetwork
from cdktf_cdktf_provider_google.compute_subnetwork import (
    ComputeSubnetwork,
    ComputeSubnetworkSecondaryIpRange,
)
from constructs import Construct

# from cdktf_cdktf_provider_google.vpc_access_connector import VpcAccessConnector


class Networks(Construct):
    def __init__(self, scope, id, project):
        super().__init__(scope, id)

        # VPC
        self.vpc = ComputeNetwork(
            self,
            'my_project_vpc_001',
            auto_create_subnetworks=False,
            name='my_project-vpc-001',
            project=project.name,
            routing_mode='REGIONAL',
        )
        self.vpc.import_from('my_project-vpc-001')

        # subnet
        self.common_private_subnet = ComputeSubnetwork(
            self,
            'my_project_private_subnet_001',
            ip_cidr_range='10.1.0.0/16',
            log_config={
                'aggregation_interval': 'INTERVAL_1_MIN',
                'flow_sampling': 0.5,
                'metadata': 'INCLUDE_ALL_METADATA'
            },
            name='my_project-private-subnet-001',
            network=self.vpc.id,
            private_ip_google_access=True,
            private_ipv6_google_access='DISABLE_GOOGLE_ACCESS',
            project=project.name,
            purpose='PRIVATE',
            region='asia-northeast1',
            secondary_ip_range=[
                ComputeSubnetworkSecondaryIpRange(
                    ip_cidr_range='10.169.0.0/17',
                    range_name='gke-asia-northeast1-tbk-dap-pro-0148ae88-gke-pods-cd572820',
                ),
                ComputeSubnetworkSecondaryIpRange(
                    ip_cidr_range='10.169.128.0/22',
                    range_name='gke-asia-northeast1-tbk-dap-pro-0148ae88-gke-services-cd572820',
                ),
            ],
            stack_type='IPV4_ONLY',
        )
        self.common_private_subnet.import_from('my_project-private-subnet-001')

        self.common_public_subnet = ComputeSubnetwork(
            self,
            'my_project_public_subnet_001',
            ip_cidr_range='10.0.0.0/16',
            log_config={
                'aggregation_interval': 'INTERVAL_1_MIN',
                'flow_sampling': 0.5,
                'metadata': 'INCLUDE_ALL_METADATA'
            },
            name='my_project-public-subnet-001',
            network=self.vpc.id,
            private_ip_google_access=True,
            private_ipv6_google_access='DISABLE_GOOGLE_ACCESS',
            project=project.name,
            purpose='PRIVATE',
            region='asia-northeast1',
            stack_type='IPV4_ONLY'
        )
        self.common_public_subnet.import_from('my_project-public-subnet-001')

        ComputeSubnetwork(
            self,
            'my_project_serverless_subnet_001',
            description='サーバーレスVPCアクセス用',
            ip_cidr_range='10.9.0.0/28',
            log_config={
                'aggregation_interval': 'INTERVAL_1_MIN',
                'flow_sampling': 0.5,
                'metadata': 'INCLUDE_ALL_METADATA'
            },
            name='my_project-serverless-subnet-001',
            network=self.vpc.id,
            private_ip_google_access=True,
            private_ipv6_google_access='DISABLE_GOOGLE_ACCESS',
            project=project.name,
            purpose='PRIVATE',
            region='asia-northeast1',
            stack_type='IPV4_ONLY',
        ).import_from('my_project-serverless-subnet-001')

        ComputeSubnetwork(
            self,
            'my_project_contr_subnet_001',
            description='VPC-CONNECTOR用のサブネット',
            ip_cidr_range='10.8.0.0/28',
            name='my_project-contr-subnet-001',
            log_config={
                'aggregation_interval': 'INTERVAL_1_MIN',
                'flow_sampling': 0.5,
                'metadata': 'INCLUDE_ALL_METADATA',
            },
            network=self.vpc.id,
            private_ip_google_access=True,
            private_ipv6_google_access='DISABLE_GOOGLE_ACCESS',
            project=project.name,
            purpose='PRIVATE',
            region='asia-northeast1',
            stack_type='IPV4_ONLY',
        ).import_from('my_project-contr-subnet-001')

        # VPC Serverless connector
        # エラーになってimport出来ない
        # 管理対象のリソース「my_project_connecor_01」を忘れないようにコメントとして残しておく
        # VpcAccessConnector(
        #     self,
        #     'my_project_connecor_01',
        #     name='my_project-connecor-001',
        #     network='my_project-vpc-001',
        #     project='978277524466',
        #     max_instances=10,
        #     min_instances=2,
        #     max_throughput=1000,
        #     subnet=VpcAccessConnectorSubnet(
        #         name='my_project-serverless-subnet-001',
        #     )
        # ).import_from('my_project-connecor-001')
