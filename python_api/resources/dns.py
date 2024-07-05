from cdktf_cdktf_provider_google.dns_managed_zone import (
    DnsManagedZone,
    DnsManagedZonePrivateVisibilityConfig,
    DnsManagedZonePrivateVisibilityConfigNetworks,
)
from cdktf_cdktf_provider_google.dns_response_policy import (
    DnsResponsePolicy,
    DnsResponsePolicyNetworks,
)
from cdktf_cdktf_provider_google.dns_response_policy_rule import DnsResponsePolicyRule
from constructs import Construct


class DnsManagedZones(Construct):
    def __init__(self, scope, id, project, vpc):
        super().__init__(scope, id)

        # DNS
        DnsManagedZone(
            self,
            'my_project_ar_google_api_dns',
            description='Artifact Registry用。VPC-SC対応。',
            dns_name='pkg.dev.',
            force_destroy=False,
            name='my_project-ar-google-api-dns',
            project=project.name,
            visibility='private',
            private_visibility_config=DnsManagedZonePrivateVisibilityConfig(
                networks=[
                    DnsManagedZonePrivateVisibilityConfigNetworks(
                        network_url=vpc.id
                    ),
                ],
            ),
        ).import_from('my_project-ar-google-api-dns')

        DnsManagedZone(
            self,
            'my_project_cf_google_api_dns',
            description='Cloud Functions用。VPC-SC対応。',
            dns_name='cloudfunctions.net.',
            force_destroy=False,
            name='my_project-cf-google-api-dns',
            project=project.name,
            visibility='private',
            private_visibility_config=DnsManagedZonePrivateVisibilityConfig(
                networks=[
                    DnsManagedZonePrivateVisibilityConfigNetworks(
                        network_url=vpc.id
                    ),
                ],
            ),
        ).import_from('my_project-cf-google-api-dns')

        DnsManagedZone(
            self,
            'my_project_cr_google_api_dns',
            description='Cloud Registry用。VPC-SC対応。',
            dns_name='gcr.io.',
            force_destroy=False,
            name='my_project-cr-google-api-dns',
            project=project.name,
            visibility='private',
            private_visibility_config=DnsManagedZonePrivateVisibilityConfig(
                networks=[
                    DnsManagedZonePrivateVisibilityConfigNetworks(
                        network_url=vpc.id
                    ),
                ],
            ),
        ).import_from('my_project-cr-google-api-dns')

        DnsManagedZone(
            self,
            'my_project_crun_google_api_dns',
            description='Cloud Run用。VPC-SC対応。',
            dns_name='run.app.',
            force_destroy=False,
            name='my_project-crun-google-api-dns',
            project=project.name,
            visibility='private',
            private_visibility_config=DnsManagedZonePrivateVisibilityConfig(
                networks=[
                    DnsManagedZonePrivateVisibilityConfigNetworks(
                        network_url=vpc.id
                    ),
                ],
            ),
        ).import_from('my_project-crun-google-api-dns')

        DnsManagedZone(
            self,
            'my_project_vawb_google_api_dns_01',
            description='Vertex AI Workbench用。VPC-SC対応。',
            dns_name='notebooks.googleapis.com.',
            force_destroy=False,
            name='my_project-vawb-google-api-dns-01',
            project=project.name,
            visibility='private',
            private_visibility_config=DnsManagedZonePrivateVisibilityConfig(
                networks=[
                    DnsManagedZonePrivateVisibilityConfigNetworks(
                        network_url=vpc.id
                    ),
                ],
            ),
        ).import_from('my_project-vawb-google-api-dns-01')

        DnsManagedZone(
            self,
            'my_project_vawb_google_api_dns_02',
            description='Vertex AI Workbench用。VPC-SC対応。',
            dns_name='notebooks.cloud.google.com.',
            force_destroy=False,
            name='my_project-vawb-google-api-dns-02',
            project=project.name,
            visibility='private',
            private_visibility_config=DnsManagedZonePrivateVisibilityConfig(
                networks=[
                    DnsManagedZonePrivateVisibilityConfigNetworks(
                        network_url=vpc.id
                    ),
                ],
            ),
        ).import_from('my_project-vawb-google-api-dns-02')

        DnsManagedZone(
            self,
            'my_project_vawb_google_api_dns_03',
            description='Vertex AI Workbench用。VPC-SC対応。',
            dns_name='notebooks.googleusercontent.com.',
            force_destroy=False,
            name='my_project-vawb-google-api-dns-03',
            project=project.name,
            visibility='private',
            private_visibility_config=DnsManagedZonePrivateVisibilityConfig(
                networks=[
                    DnsManagedZonePrivateVisibilityConfigNetworks(
                        network_url=vpc.id
                    ),
                ],
            ),
        ).import_from('my_project-vawb-google-api-dns-03')


class DnsResponsePolicies(Construct):
    def __init__(self, scope, id, project, vpc):
        super().__init__(scope, id)

        _googleapis_response_policy = DnsResponsePolicy(
            self,
            'my_project_googleapis_response_policy',
            networks=[DnsResponsePolicyNetworks(network_url=vpc.self_link)],
            project=project.number,
            response_policy_name='my_project-googleapis-response-policy',
        )
        _googleapis_response_policy.import_from(
            'projects/978277524466/responsePolicies/my_project-googleapis-response-policy')

        DnsResponsePolicyRule(
            self,
            'my_project_dataformapi_policy_rule',
            depends_on=[_googleapis_response_policy],
            dns_name='dataform.googleapis.com.',
            local_data={
                'local_datas': [{
                    'name': 'dataform.googleapis.com.',
                    'rrdatas': ['private.googleapis.com.'],
                    'ttl': 300,
                    'type': 'CNAME'
                }],
            },
            project=project.number,
            response_policy=_googleapis_response_policy.response_policy_name,
            rule_name='my_project-dataformapi-policy-rule',
        ).import_from('projects/978277524466/responsePolicies/my_project-googleapis-response-policy/rules/my_project-dataformapi-policy-rule')

        DnsResponsePolicyRule(
            self,
            'my_project_googleapis_policy_rule',
            depends_on=[_googleapis_response_policy],
            dns_name='*.googleapis.com.',
            local_data={
                'local_datas': [{
                    'name': '*.googleapis.com.',
                    'rrdatas': ['199.36.153.4', '199.36.153.5', '199.36.153.6', '199.36.153.7'],
                    'ttl': 300,
                    'type': 'A'
                }],
            },
            project=project.number,
            response_policy=_googleapis_response_policy.response_policy_name,
            rule_name='my_project-googleapis-policy-rule',
        ).import_from('projects/978277524466/responsePolicies/my_project-googleapis-response-policy/rules/my_project-googleapis-policy-rule')

        DnsResponsePolicyRule(
            self,
            'my_project_privateapis_policy_rule',
            depends_on=[_googleapis_response_policy],
            dns_name='private.googleapis.com.',
            local_data={
                'local_datas': [{
                    'name': 'private.googleapis.com.',
                    'rrdatas': ['199.36.153.8', '199.36.153.9', '199.36.153.10', '199.36.153.11'],
                    'ttl': 300,
                    'type': 'A'
                }],
            },
            project=project.number,
            response_policy=_googleapis_response_policy.response_policy_name,
            rule_name='my_project-privateapis-policy-rule',
        ).import_from('projects/978277524466/responsePolicies/my_project-googleapis-response-policy/rules/my_project-privateapis-policy-rule')

        DnsResponsePolicyRule(
            self,
            'my_project_searchconsoleapi_policy_rule',
            depends_on=[_googleapis_response_policy],
            dns_name='searchconsole.googleapis.com.',
            local_data={
                'local_datas': [{
                    'name': 'searchconsole.googleapis.com.',
                    'rrdatas': ['private.googleapis.com.'],
                    'ttl': 300,
                    'type': 'CNAME'
                }],
            },
            project=project.number,
            response_policy=_googleapis_response_policy.response_policy_name,
            rule_name='my_project-searchconsoleapi-policy-rule',
        ).import_from('projects/978277524466/responsePolicies/my_project-googleapis-response-policy/rules/my_project-searchconsoleapi-policy-rule')

        DnsResponsePolicyRule(
            self,
            'my_project_sheetsapi_policy_rule',
            depends_on=[_googleapis_response_policy],
            dns_name='sheets.googleapis.com.',
            local_data={
                'local_datas': [{
                    'name': 'sheets.googleapis.com.',
                    'rrdatas': ['private.googleapis.com.'],
                    'ttl': 300,
                    'type': 'CNAME'
                }],
            },
            project=project.number,
            response_policy=_googleapis_response_policy.response_policy_name,
            rule_name='my_project-sheetsapi-policy-rule',
        ).import_from('projects/978277524466/responsePolicies/my_project-googleapis-response-policy/rules/my_project-sheetsapi-policy-rule')

        DnsResponsePolicyRule(
            self,
            'my_project_wwwapi_policy_rule',
            depends_on=[_googleapis_response_policy],
            dns_name='www.googleapis.com.',
            local_data={
                'local_datas': [{
                    'name': 'www.googleapis.com.',
                    'rrdatas': ['private.googleapis.com.'],
                    'ttl': 300,
                    'type': 'CNAME'
                }],
            },
            project=project.number,
            response_policy=_googleapis_response_policy.response_policy_name,
            rule_name='my_project-wwwapi-policy-rule',
        ).import_from('projects/978277524466/responsePolicies/my_project-googleapis-response-policy/rules/my_project-wwwapi-policy-rule')
