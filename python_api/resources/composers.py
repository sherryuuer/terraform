from cdktf_cdktf_provider_google.composer_environment import (
    ComposerEnvironment,
    ComposerEnvironmentConfigA,
    ComposerEnvironmentConfigMaintenanceWindow,
    ComposerEnvironmentConfigNodeConfig,
    ComposerEnvironmentConfigPrivateEnvironmentConfig,
    ComposerEnvironmentConfigRecoveryConfig,
    ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig,
    ComposerEnvironmentConfigSoftwareConfig,
    ComposerEnvironmentConfigWebServerNetworkAccessControl,
    ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange,
    ComposerEnvironmentConfigWorkloadsConfig,
    ComposerEnvironmentConfigWorkloadsConfigScheduler,
    ComposerEnvironmentConfigWorkloadsConfigTriggerer,
    ComposerEnvironmentConfigWorkloadsConfigWebServer,
    ComposerEnvironmentConfigWorkloadsConfigWorker,
)
from constructs import Construct


class Composers(Construct):
    def __init__(self, scope, id, vpc, private_subnet):
        super().__init__(scope, id)

        # Composer
        # 環境名に利用。prod or devを記載する。
        ENV = 'prod'
        # 環境名に利用。01 or 001を記載する。新環境と既存環境の名前を替えて共存させる為。
        ENV_SEQ = '01'
        # Airflow構成のオーバーライド
        AIRFLOW_CONFIG_OVERRIDES = {
            'webserver-default_ui_timezone': 'Asia/Tokyo',
            'core-max_active_runs_per_dag': '100',
            'core-non_pooled_task_slot_count': '36',
            'core-default_timezone': 'Asia/Tokyo',
            'core-min_serialized_dag_update_interval': '30',
            'core-parallelism': '36',
            'core-max_active_tasks_per_dag': '20',
            'core-dag_file_processor_timeout': '150',
            'email-from_email': 'ad@trustbank.co.jp',
            'email-email_conn_id': 'sendgrid_default',
            'scheduler-parsing_processes': '6',
            'scheduler-dag_dir_list_interval': '30',
        }
        # PYPIパッケージインストール
        # 環境のupdateの際にはパッケージもupdateすること
        PYPI_PACKAGES = {
            # DS管理
            'annoy': '==1.17.0',
            'gensim': '==4.2.0',

            # DI管理
            'apache-airflow-providers-sftp': '==4.0.0',
            'apache-airflow-providers-ssh': '==2.4.4',
            'openpyxl': '==3.0.10',
            'pdfrw': '==0.4',
            'pikepdf': '==5.4.2',
            'pypdf': '==3.17.0',
            'reportlab': '==4.0.4',
            'slackweb': '==1.0.5',
            'tableauserverclient': '==0.19.0',
        }
        # Airflowウェブサーバーのアクセス制御
        AIRFLOW_WEBSERVER_ALLOWED_IPS = {
            '118.238.245.247': 'ジールVPNメイン',
            '113.43.139.80': 'ジールVPNバックアップ',
            # '150.195.208.13': 'トラストバンクVPN(CATO)',
            # '150.195.210.66': 'トラストバンクVPN(CATO)',

            # 削除予定のIP
            '176.34.27.223': 'トラストバンク',
            '18.178.46.217': 'トラストバンク',
            '163.116.128.0/17': 'トラストバンク新VPN',
            '150.195.208.13': 'トラストバンク新VPN(CATO)',
            '150.195.210.66': 'トラストバンク新VPN(CATO)',
            '163.116.208.0/24': 'トラストバンク新VPN（20230120更新）',
            '103.219.79.0/24': 'トラストバンク様廃棄予定のIP',
            '18.182.247.11': '高島さんテストIP',
        }

        ComposerEnvironment(
            self,
            'composer',
            name=f'tbk-dap-{ENV}-composer-{ENV_SEQ}',
            region='asia-northeast1',
            config=ComposerEnvironmentConfigA(
                node_config=ComposerEnvironmentConfigNodeConfig(
                    network=vpc.id,
                    subnetwork=private_subnet.id,
                    service_account='my_project-composer-sa@my_project.iam.gserviceaccount.com',
                    tags=['my_project-composer-01'],
                ),
                software_config=ComposerEnvironmentConfigSoftwareConfig(
                    airflow_config_overrides=AIRFLOW_CONFIG_OVERRIDES,
                    pypi_packages=PYPI_PACKAGES,
                    image_version='composer-2.4.1-airflow-2.5.3',
                ),
                private_environment_config=ComposerEnvironmentConfigPrivateEnvironmentConfig(
                    connection_type='PRIVATE_SERVICE_CONNECT',
                    enable_privately_used_public_ips=False,
                    enable_private_endpoint=False,
                    cloud_composer_connection_subnetwork=private_subnet.id
                ),
                web_server_network_access_control=ComposerEnvironmentConfigWebServerNetworkAccessControl(
                    allowed_ip_range=[
                        ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange(
                            value=key,
                            description=value,
                        ) for key, value in AIRFLOW_WEBSERVER_ALLOWED_IPS.items()
                    ]
                ),
                maintenance_window=ComposerEnvironmentConfigMaintenanceWindow(
                    # start_time、end_time共に時間のみ利用される
                    # 日付は無視されるが、日付を指定しないとエラーになるので注意
                    start_time='2023-08-27T03:00:00Z',
                    end_time='2023-08-27T07:00:00Z',
                    recurrence='FREQ=WEEKLY;BYDAY=FR,SA,SU',
                ),
                workloads_config=ComposerEnvironmentConfigWorkloadsConfig(
                    scheduler=ComposerEnvironmentConfigWorkloadsConfigScheduler(
                        cpu=2,
                        memory_gb=4,
                        storage_gb=2,
                        count=1,
                    ),
                    web_server=ComposerEnvironmentConfigWorkloadsConfigWebServer(
                        cpu=1,
                        memory_gb=1.5,
                        storage_gb=1,
                    ),
                    worker=ComposerEnvironmentConfigWorkloadsConfigWorker(
                        cpu=4,
                        memory_gb=12,
                        storage_gb=2,
                        min_count=1,
                        max_count=2,
                    ),
                    triggerer=ComposerEnvironmentConfigWorkloadsConfigTriggerer(
                        cpu=0.5,
                        memory_gb=0.5,
                        count=1,
                    )
                ),
                environment_size='ENVIRONMENT_SIZE_SMALL',
                # master_authorized_networks_config=ComposerEnvironmentConfigMasterAuthorizedNetworksConfig(
                #     enabled=True,
                # )
                recovery_config=ComposerEnvironmentConfigRecoveryConfig(
                    scheduled_snapshots_config=ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig(
                        enabled=False),
                ),
            )
        ).import_from('projects/my_project/locations/asia-northeast1/environments/my_project-composer-01')
