from cdktf_cdktf_provider_google.compute_address import ComputeAddress
from cdktf_cdktf_provider_google.compute_disk import ComputeDisk
from cdktf_cdktf_provider_google.compute_disk_resource_policy_attachment import (
    ComputeDiskResourcePolicyAttachment,
)
from cdktf_cdktf_provider_google.compute_firewall import ComputeFirewall
from cdktf_cdktf_provider_google.compute_global_address import ComputeGlobalAddress
from cdktf_cdktf_provider_google.compute_instance import (
    ComputeInstance,
    ComputeInstanceNetworkInterface,
    ComputeInstanceNetworkInterfaceAccessConfig,
)
from cdktf_cdktf_provider_google.compute_resource_policy import ComputeResourcePolicy
from constructs import Construct


class Computes(Construct):
    def __init__(self, scope, id, project, vpc, public_subnet, private_subnet):
        super().__init__(scope, id)

        # IPアドレス
        _sftp_server_ip = ComputeAddress(
            self,
            'sftp_server_ip',
            address='10.1.0.9',
            address_type='INTERNAL',
            name='sftp-server-ip',
            network_tier='PREMIUM',
            project=project.name,
            purpose='GCE_ENDPOINT',
            region='asia-northeast1',
            subnetwork=private_subnet.id,
        )
        _sftp_server_ip.import_from('sftp-server-ip')

        # Compute Disk
        _disc_bastion_gce_01 = ComputeDisk(
            self,
            "disks_my_project_bastion_gce_01",
            guest_os_features=[
                {"type": "UEFI_COMPATIBLE"},
                {"type": "VIRTIO_SCSI_MULTIQUEUE"},
            ],
            image="https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/debian-10-buster-v20200910",
            licenses=[
                "https://www.googleapis.com/compute/v1/projects/debian-cloud/global/licenses/debian-10-buster"],
            name="my_project-bastion-gce-01",
            physical_block_size_bytes=4096,
            project=project.name,
            provisioned_iops=0,
            provisioned_throughput=0,
            size=10,
            type="pd-standard",
            zone="asia-northeast1-a"
        )
        _disc_bastion_gce_01.import_from(
            'projects/my_project/zones/asia-northeast1-a/disks/my_project-bastion-gce-01')

        _disc_sftp_gce_01 = ComputeDisk(
            self,
            "disks_my_project_sftp_gce_01",
            guest_os_features=[
                {"type": "UEFI_COMPATIBLE"},
                {"type": "VIRTIO_SCSI_MULTIQUEUE"},
            ],
            image="https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/debian-10-buster-v20200910",
            licenses=[
                "https://www.googleapis.com/compute/v1/projects/debian-cloud/global/licenses/debian-10-buster"],
            name="my_project-sftp-gce-01",
            physical_block_size_bytes=4096,
            project=project.name,
            provisioned_iops=0,
            provisioned_throughput=0,
            size=100,
            type="pd-standard",
            zone="asia-northeast1-a"
        )
        _disc_sftp_gce_01.import_from(
            'projects/my_project/zones/asia-northeast1-a/disks/my_project-sftp-gce-01')

        # GCE
        ComputeInstance(
            self,
            'my_project_bastion_gce_01',
            boot_disk={
                'auto_delete': True,
                'device_name': _disc_bastion_gce_01.name,
                'initialize_params': {
                    'image': 'https://www.googleapis.com/compute/beta/projects/debian-cloud/global/images/debian-10-buster-v20200910',
                    'size': 10,
                    'type': 'pd-standard',
                },
                'mode': 'READ_WRITE',
                'source': _disc_bastion_gce_01.self_link,
            },
            confidential_instance_config={
                'enable_confidential_compute': False
            },
            deletion_protection=True,
            machine_type='e2-standard-2',
            metadata={
                'block-project-ssh-keys': 'true',
                'ssh-keys': (
                    'bastion:ssh-rsa '
                    'AAAAB3NzaC1yc2EAAAABIwAAAQEAywRFJc3SMb7KdA1Tv9/lKg3KrDaPswOdtdbgXukNS3Sd6JiFid5UNAmDVyK3TjiF1JuioI/i49veZPR6uM8Z9QvRaxOCcewPLxuqS2/'
                    'gbigZdWcg5ajtBq3ntRoBy4M0C+G53vqjQGOxhFmA6LFNXFkYLp9pqqtVL7KYlOHyrSbn9EfHBaqbgjr68rEStVIWs+LkdAVsB/FO0GVQlKiIRlSk+3gC7yMZ4pE6GI5KX8AxWw71TFXSRd9oHipOiborJ5grR1KQG5yFhBFu0PAxuqjO/'
                    'U8WxRpHh7W7noJTnramkUm67mAbPYVTVneBi1phvm4hzunP3EzrBBs9Zb2/kw== bastion'
                )
            },
            name='my_project-bastion-gce-01',
            network_interface=[
                ComputeInstanceNetworkInterface(
                    network=vpc.id,
                    network_ip='10.0.0.2',
                    subnetwork=public_subnet.id,
                    subnetwork_project=project.name,
                    access_config=[
                        ComputeInstanceNetworkInterfaceAccessConfig(
                            nat_ip='34.84.198.230',
                            network_tier='PREMIUM',
                        ),
                    ]
                ),
            ],
            project=project.name,
            reservation_affinity={
                'type': 'ANY_RESERVATION',
            },
            scheduling={
                'automatic_restart': True,
                'on_host_maintenance': 'MIGRATE',
                'provisioning_model': 'STANDARD',
            },
            service_account={
                'email': 'my_project-bastion-sa@my_project.iam.gserviceaccount.com',
                'scopes': ['https://www.googleapis.com/auth/cloud-platform'],
            },
            shielded_instance_config={
                'enable_integrity_monitoring': True,
                'enable_vtpm': True,
            },
            tags=['bastion'],
            # zoneは設定するとなぜかエラーになるのでコメントアウトしている
            # zone='asia-northeast1-a'
        ).import_from('my_project-bastion-gce-01')

        ComputeInstance(
            self,
            'my_project_sftp_gce_01',
            boot_disk={
                'auto_delete': True,
                'device_name': _disc_sftp_gce_01.name,
                'initialize_params': {
                    'image': 'https://www.googleapis.com/compute/beta/projects/debian-cloud/global/images/debian-10-buster-v20200910',
                    'size': 100,
                    'type': 'pd-standard',
                },
                'mode': 'READ_WRITE',
                'source': _disc_sftp_gce_01.self_link,
            },
            confidential_instance_config={
                'enable_confidential_compute': False,
            },
            deletion_protection=True,
            machine_type='e2-standard-2',
            metadata={
                'block-project-ssh-keys': 'true',
                'ssh-keys': (
                    'sftp:ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA4ci6VbjSFFHRQ0bLEbVv7I1Ninyjj6/'
                    '+JP1TT6adAYvKOWG/oso1FtkBds6sK4HTG/P34ifcpAsEIkNDiDE92LtbYIq+lTulVxKg1LfRSC+RhV0hQ0iTKpEq17knlGKTplxBsweKlRUIIhURZcXiACsmmiVTgawbjDTPQUd99RoNdDCY3wj8qcCwQzMujQowMfXo9/'
                    'yek6xdo0bNE1zlh8QJ/+MdMBxscD9mybJQNYx7pg9CdTZWbCagjCgZWvPlxIw79QVofswuFbtSZO8wij8wVyxV9RCChEui5mvJlsb9rmQzGGbHoojpEupTaq76gKWG/I1AnUqb0ce+HzGY/Q== sftp'
                ),
            },
            name='my_project-sftp-gce-01',
            network_interface=[
                ComputeInstanceNetworkInterface(
                    network=vpc.id,
                    network_ip=_sftp_server_ip.address,
                    subnetwork=private_subnet.id,
                    subnetwork_project=project.name,
                ),
            ],
            project=project.name,
            reservation_affinity={
                'type': 'ANY_RESERVATION'
            },
            scheduling={
                'automatic_restart': True,
                'on_host_maintenance': 'MIGRATE',
                'provisioning_model': 'STANDARD',
            },
            service_account={
                'email': 'my_project-sftp-sa@my_project.iam.gserviceaccount.com',
                'scopes': ['https://www.googleapis.com/auth/cloud-platform'],
            },
            shielded_instance_config={
                'enable_integrity_monitoring': True,
                'enable_vtpm': True,
            },
            tags=['sftp'],
            # zoneは設定するとなぜかエラーになるのでコメントアウトしている
            # zone='asia-northeast1-a',
        ).import_from('my_project-sftp-gce-01')

        # GCEリソースポリシー
        _snapshot_schedule_resource_policy = ComputeResourcePolicy(
            self,
            'my_project_gce_01_snapshot_schedule_1',
            name='my_project-gce-01-snapshot-schedule-1',
            project=project.name,
            region='asia-northeast1',
            snapshot_schedule_policy={
                'retention_policy': {
                    'max_retention_days': 14,
                    'on_source_disk_delete': 'KEEP_AUTO_SNAPSHOTS',
                },
                'schedule': {
                    'daily_schedule': {
                        'days_in_cycle': 1,
                        'start_time': '15:00',
                    }
                },
                'snapshot_properties': {
                    'storage_locations': ['asia-northeast1'],
                },
            },
        )
        _snapshot_schedule_resource_policy.import_from(
            'my_project-gce-01-snapshot-schedule-1')

        ComputeDiskResourcePolicyAttachment(
            self,
            "my_project_bastion_gce_01_snapshot_schedule_1_resource_policy_attach",
            disk=_disc_bastion_gce_01.name,
            name=_snapshot_schedule_resource_policy.name,
            project=project.name,
            zone="asia-northeast1-a",
        ).import_from('projects/my_project/zones/asia-northeast1-a/disks/my_project-bastion-gce-01/my_project-gce-01-snapshot-schedule-1')

        ComputeDiskResourcePolicyAttachment(
            self,
            "my_project_sftp_gce_01_snapshot_schedule_1_resource_policy_attach",
            disk=_disc_sftp_gce_01.name,
            name=_snapshot_schedule_resource_policy.name,
            project=project.name,
            zone="asia-northeast1-a",
        ).import_from('projects/my_project/zones/asia-northeast1-a/disks/my_project-sftp-gce-01/my_project-gce-01-snapshot-schedule-1')

        # Global Address
        ComputeGlobalAddress(
            self,
            'my_project_googleapis_psc_ip',
            address='10.255.0.1',
            address_type='INTERNAL',
            name='my_project-googleapis-psc-ip',
            network=vpc.id,
            prefix_length=0,
            project='my_project',
            purpose='PRIVATE_SERVICE_CONNECT',
        ).import_from('projects/my_project/global/addresses/my_project-googleapis-psc-ip')

        ComputeGlobalAddress(
            self,
            'my_project_private_service_01',
            address='10.9.1.0',
            address_type='INTERNAL',
            name='my_project-private-service-01',
            network=vpc.id,
            prefix_length=24,
            project='my_project',
            purpose='VPC_PEERING',
        ).import_from('projects/my_project/global/addresses/my_project-private-service-01')

        ComputeGlobalAddress(
            self,
            'my_project_private_service_02',
            address='10.9.2.0',
            address_type='INTERNAL',
            name='my_project-private-service-02',
            network=vpc.id,
            prefix_length=24,
            project='my_project',
            purpose='VPC_PEERING',
        ).import_from('projects/my_project/global/addresses/my_project-private-service-02')


class ComputeFirewalls(Construct):
    def __init__(self, scope, id, project, vpc):
        super().__init__(scope, id)

        ComputeFirewall(
            self,
            'allow_ingress_from_iap',
            allow=[
                {
                    'ports': ['22', '3389'],
                    'protocol': 'tcp',
                },
            ],
            direction='INGRESS',
            name='allow-ingress-from-iap',
            network=vpc.id,
            priority=998,
            project=project.name,
            source_ranges=[
                '130.211.0.0/22',
                '35.191.0.0/16',
                '35.235.240.0/20',
            ],
        ).import_from('allow-ingress-from-iap')

        ComputeFirewall(
            self,
            'my_project_bastion_egress_deny_fw',
            deny=[{'protocol': 'all'}],
            description='踏み台サーバーの下り禁止',
            destination_ranges=['0.0.0.0/0'],
            direction='EGRESS',
            name='my_project-bastion-egress-deny-fw',
            network=vpc.id,
            priority=60000,
            project=project.name,
            target_tags=['bastion'],
        ).import_from('my_project-bastion-egress-deny-fw')

        ComputeFirewall(
            self,
            'my_project_bastion_ssh_allow_fw',
            allow=[
                {
                    'ports': ['22', '10022'],
                    'protocol': 'tcp',
                },
            ],
            description='bastionサーバー用ssh許可',
            direction='INGRESS',
            name='my_project-bastion-ssh-allow-fw',
            network=vpc.id,
            priority=1000,
            project=project.name,
            source_ranges=[
                '101.110.58.41',
                '113.36.2.114',
                '113.43.139.80',
                '118.238.245.247',
                '118.238.250.198',
                '13.230.58.133',
                '150.195.208.13',
                '150.195.210.66',
                '176.34.27.223',
                '18.178.46.217',
                '34.84.198.230',
                '52.198.20.20',
                '59.106.234.5',
            ],
            target_tags=['bastion'],
        ).import_from('my_project-bastion-ssh-allow-fw')

        ComputeFirewall(
            self,
            'my_project_bastion_ssh_egress_allow_fw',
            allow=[
                {
                    'ports': ['22'],
                    'protocol': 'tcp',
                },
            ],
            description='踏み台サーバーのSSH下り許可',
            destination_ranges=['10.1.0.0/16'],
            direction='EGRESS',
            name='my_project-bastion-ssh-egress-allow-fw',
            network=vpc.id,
            priority=10000,
            project=project.name,
            target_tags=['bastion'],
        ).import_from('my_project-bastion-ssh-egress-allow-fw')

        ComputeFirewall(
            self,
            'my_project_composer_health_check_http_allow_fw',
            allow=[
                {
                    'ports': ['80', '443'],
                    'protocol': 'tcp',
                },
            ],
            description='composerへのGCPヘルスチェック用。vpcサービスコントロール内にcomposer環境を作成する為に設定。',
            direction='INGRESS',
            name='my_project-composer-health-check-http-allow-fw',
            network=vpc.id,
            priority=1000,
            project=project.name,
            source_ranges=[
                '130.211.0.0/22',
                '35.191.0.0/16',
            ],
            target_tags=['my_project-composer-01'],
        ).import_from('my_project-composer-health-check-http-allow-fw')

        ComputeFirewall(
            self,
            'my_project_sftp_egress_deny_fw',
            deny=[{'protocol': 'all'}],
            description='sftpサーバー下り禁止',
            destination_ranges=['0.0.0.0/0'],
            direction='EGRESS',
            name='my_project-sftp-egress-deny-fw',
            network=vpc.id,
            priority=60000,
            project=project.name,
            target_tags=['sftp'],
        ).import_from('my_project-sftp-egress-deny-fw')

        ComputeFirewall(
            self,
            'my_project_sftp_google_api_egress_allow_fw',
            allow=[
                {
                    'ports': ['443'],
                    'protocol': 'tcp',
                },
            ],
            description='sftpサーバーからgoogleAPIへのhttps下り接続許可',
            destination_ranges=['199.36.153.4/30'],
            direction='EGRESS',
            name='my_project-sftp-google-api-egress-allow-fw',
            network=vpc.id,
            priority=10000,
            project=project.name,
            target_tags=['sftp'],
        ).import_from('my_project-sftp-google-api-egress-allow-fw')

        ComputeFirewall(
            self,
            'my_project_sftp_ssh_allow_fw',
            allow=[
                {
                    'ports': ['22'],
                    'protocol': 'tcp',
                },
            ],
            description='sftpサーバー用ssh許可',
            direction='INGRESS',
            name='my_project-sftp-ssh-allow-fw',
            network=vpc.id,
            priority=1000,
            project=project.name,
            source_ranges=[
                '10.0.0.0/16',
                '10.124.0.0/14',
                '10.169.0.0/17',
                '10.44.0.0/14',
            ],
            target_tags=['sftp'],
        ).import_from('my_project-sftp-ssh-allow-fw')
