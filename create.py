import json
import random
import time
import requests
import re
from alibabacloud_cloudcontrol20220830.client import Client as cloudcontrol20220830Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cloudcontrol20220830 import models as cloudcontrol_20220830_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_20140526_models

region_zone_dict = {
    'cn-qingdao': ['cn-qingdao-b','cn-qingdao-c'],
    'cn-beijing': ['cn-beijing-a', 'cn-beijing-b', 'cn-beijing-c', 'cn-beijing-d', 'cn-beijing-e', 'cn-beijing-f','cn-beijing-g', 'cn-beijing-h', 'cn-beijing-i', 'cn-beijing-j', 'cn-beijing-k', 'cn-beijing-l'],
    'cn-zhangjiakou': ['cn-zhangjiakou-a','cn-zhangjiakou-b','cn-zhangjiakou-c'],
    'cn-huhehaote': ['cn-huhehaote-a','cn-huhehaote-b'],
    'cn-wulanchabu': ['cn-wulanchabu-a','cn-wulanchabu-b','cn-wulanchabu-c'],
    'cn-hangzhou': ['cn-hangzhou-e','cn-hangzhou-b','cn-hangzhou-f','cn-hangzhou-g','cn-hangzhou-h','cn-hangzhou-i','cn-hangzhou-j','cn-hangzhou-k'],
    'cn-shanghai': ['cn-shanghai-a','cn-shanghai-b','cn-shanghai-c','cn-shanghai-d','cn-shanghai-e','cn-shanghai-f','cn-shanghai-g','cn-shanghai-k','cn-shanghai-l','cn-shanghai-m','cn-shanghai-n'],
    'cn-nanjing': ['cn-nanjing-a'],
    'cn-fuzhou': ['cn-fuzhou-a'],
    'cn-shenzhen': ['cn-shenzhen-a','cn-shenzhen-b','cn-shenzhen-c','cn-shenzhen-d','cn-shenzhen-e','cn-shenzhen-f'],
    'cn-heyuan': ['cn-heyuan-a','cn-heyuan-b'],
    'cn-guangzhou': ['cn-guangzhou-a','cn-guangzhou-b'],
    'cn-chengdu': ['cn-chengdu-a','cn-chengdu-b'],
    'cn-hongkong': ['cn-hongkong-a','cn-hongkong-b','cn-hongkong-c'],
    'ap-southeast-1': ['ap-southeast-1-a','ap-southeast-1-b','ap-southeast-1-c'],
    'ap-southeast-2': ['ap-southeast-2-a','ap-southeast-2-b'],
    'ap-southeast-3': ['ap-southeast-3-a','ap-southeast-3-b'],
    'ap-southeast-5': ['ap-southeast-5-a','ap-southeast-5-b','ap-southeast-5-c'],
    'ap-southeast-6': ['ap-southeast-6-a'],
    'ap-southeast-7': ['ap-southeast-7-a'],
    'ap-south-1': ['ap-south-1-a','ap-south-1-b'],
    'ap-northeast-1': ['ap-northeast-1-a','ap-northeast-1-b','ap-northeast-1-c'],
    'ap-northeast-2': ['ap-northeast-2-a'],
    'us-west-1': ['us-west-1-a','us-west-1-b'],
    'us-east-1': ['us-east-1-a','us-east-1-b'],
    'eu-central-1': ['eu-central-1-a','eu-central-1-b','eu-central-1-c'],
    'eu-west-1': ['eu-west-1-a','eu-west-1-b'],
    'me-east-1': ['me-east-1-a'],
}

class Sample:

    @staticmethod
    def create_client1(access_key_id: str,access_key_secret: str,) -> cloudcontrol20220830Client:
        config = open_api_models.Config(access_key_id=access_key_id,access_key_secret=access_key_secret)
        config.endpoint = f'cloudcontrol.aliyuncs.com'
        return cloudcontrol20220830Client(config)

    @staticmethod
    def create_client2(access_key_id: str,access_key_secret: str,) -> Ecs20140526Client:
        config = open_api_models.Config(access_key_id=access_key_id,access_key_secret=access_key_secret)
        config.endpoint = f'ecs-cn-hangzhou.aliyuncs.com'
        return Ecs20140526Client(config)

    @staticmethod
    def create_client3(access_key_id: str,access_key_secret: str,) -> cloudcontrol20220830Client:
        config = open_api_models.Config(access_key_id=access_key_id,access_key_secret=access_key_secret)
        config.endpoint = f'cloudcontrol.aliyuncs.com'
        return cloudcontrol20220830Client(config)

    @staticmethod
    def create():
        client = Sample.create_client1('aaa', 'bbb')#输入你的key
        request_path = '/api/v1/providers/Aliyun/products/ECS/resources/Instance'
        body = {
            'InstanceNetworkType': 'vpc',
            'ImageId': 'ubuntu_22_04_x64_20G_alibase_20230208.vhd',
            'AutoRenewEnabled': True,
            'Status': '200',
            'RenewalStatus': 'AutoRenewal',
            'InternetChargeType': 'PayByTraffic',
            'InternetMaxBandwidthOut': 1,
            'PaymentType': 'PostPaid',
            'ZoneId': zon,
            'InternetMaxBandwidthIn': 100,
            'CreditSpecification': 'Standard',

        }
        create_resource_request = cloudcontrol_20220830_models.CreateResourceRequest(
            region_id=reg,
            body=body
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            aa=client.create_resource_with_options(request_path, create_resource_request, headers, runtime)
            response_str = str(aa)
            id = re.search(r"resourceId': '(.*?)', ", response_str)
            id = id.group(1)
        except Exception as error:
            UtilClient.assert_as_string(error.message)
            print(error.message)

        return id

    @staticmethod
    def publicip(id):
        client = Sample.create_client2('aaa', 'bbb')
        allocate_public_ip_address_request = ecs_20140526_models.AllocatePublicIpAddressRequest(
            instance_id=id
        )
        runtime = util_models.RuntimeOptions()

        bb=client.allocate_public_ip_address_with_options(allocate_public_ip_address_request, runtime)
        print(f"id:{id} 赋值公网IP成功！")
        response_str = str(bb)
        ip = re.search(r"'IpAddress': '(.*?)', ", response_str)
        ip = ip.group(1)

        return ip

    @staticmethod
    def delete(id):
        client = Sample.create_client3('aaa', 'bbb')
        request_path = '/api/v1/providers/Aliyun/products/ECS/resources/Instance/'+id
        delete_resource_request = cloudcontrol_20220830_models.DeleteResourceRequest(region_id=reg)
        runtime = util_models.RuntimeOptions()
        headers = {}
        client.delete_resource_with_options(request_path, delete_resource_request, headers, runtime)
        print(f"id:{id}删除成功！！")


for i in range(0,15):

    reg = "cn-beijing"
    zon = "cn-beijing-c"

    print(f"第{i}次")
    try:
        id = Sample.create()
        ip = Sample.publicip(id)
        #print(ip)
    except:
        continue
    print(ip)

    while True:
        try:
            Sample.delete(id)
            break
        except:
            print("诶呀删不掉，等10s再试一次！")
            time.sleep(10)
            continue