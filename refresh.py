# -*- coding: utf-8 -*-
from __future__ import print_function

from botocore.exceptions import ClientError
from requests import get
import boto3


class Aws:
    def __init__(self, profile):
        self.profile = profile

    def __getBoto(self):
        return boto3.Session(profile_name=self.profile)

    def securityGroup(self, security):
        return self.__getBoto().resource('ec2').SecurityGroup(security)

    def authorize_ip(self, security, external_ip, description):
        try:
            response = self.securityGroup(security).authorize_ingress(
                DryRun=False,
                IpPermissions=[
                    {
                        'FromPort': 3306,
                        'ToPort': 3306,
                        'IpProtocol': "tcp",
                        'IpRanges': [
                            {
                                'CidrIp': external_ip+"/32",
                                'Description': description
                            },
                        ]
                    }
                ]
            )
        except ClientError as err:
            print("Failed authorize ingress.\n" + str(err))
            return False

        print(response)
        return True

    def revoke_ip(self, security, external_ip, description):
        try:
            response = self.securityGroup(security).revoke_ingress(
                DryRun=False,
                IpPermissions=[
                    {
                        'FromPort': 3306,
                        'ToPort': 3306,
                        'IpProtocol': "tcp",
                        'IpRanges': [
                            {
                                'CidrIp': external_ip,
                                'Description': description
                            },
                        ]
                    }
                ]
            )
        except ClientError as err:
            print("Failed revoke.\n" + str(err))
            return False

        print(response)
        return True

    def refresh_ip(self, securities_groups,  description):
        try:
            externalip = get('https://ident.me').text

            for sgs in securities_groups:
                ec2 = self.securityGroup(sgs)
                response = ec2.ip_permissions
                for sg in response:
                    for iprange in sg["IpRanges"]:
                        if 'Description' in iprange:
                            if iprange['Description'] == description:
                                print(iprange['CidrIp'])
                                self.revoke_ip(
                                    sgs, iprange['CidrIp'], description)
                                self.authorize_ip(sgs, externalip, description)

        except ClientError as e:
            print(e)


securities_groups = ["sg-XXXXXXXXXXXXX"]
aws = Aws('client')
aws.refresh_ip(securities_groups, "topic")
