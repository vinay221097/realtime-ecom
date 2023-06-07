import boto3
from botocore.config import Config
from datetime import datetime
from botocore.exceptions import ClientError
REGION='us-east-1'
config = Config(
   retries = {
      'max_attempts': 10,
      'mode': 'standard'
   }
)

db=boto3.resource('dynamodb',region_name=REGION,config=config)


data_obj={
                    "sessions":{
                        "label": '',
                        "value": 0,
                    },
                    "clicks":{
                        "label": '',
                        "value": 0,
                    },
                    "engagement_time":{
                        "label": '',
                        "value": 0,
                    },
                      "devices":{
                        "label": [0],
                        "value": [0],
                    },
                      "pages":{
                        "label": [0],
                        "value": [0],
                    },
                    "total_sessions_count":0,
                    "total_pages_count":0,
                    "total_devices_count":0
                }


def client_data(client_id):
    devices_table = db.Table('overall_hits')
    try:
        response = devices_table.get_item(
        Key={'id': client_id})
        print(response)
        if 'Item' in response.keys():
            response=response['Item']
            date_value= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if 'session_count' in response.keys():
                data_obj['sessions']={"label":date_value,"value":int(response['session_count'])}
            if 'clicks' in response.keys():
                data_obj['clicks']={"label":date_value,"value":int(response['clicks'])} 
            if 'engagement_time' in response.keys():
                data_obj['engagement_time']={"label":date_value,"value":int(response['engagement_time'])}
            if 'devices' in response.keys():
                data_obj['devices']={"label":list(response['devices'].keys()),"value":list(response['devices'].values())}
            if "pages" in response.keys():
                data_obj['pages']={"label":list(response['pages'].keys()),"value":list(response['pages'].values())}
            if "total_sessions" in response.keys():
                data_obj['total_sessions_count']=response["total_sessions"]
            if "total_pages" in response.keys():
                data_obj['total_pages_count']=response["total_pages"]
            if "total_devices" in response.keys():
                data_obj["total_devices_count"]=response["total_devices"]


    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return data_obj


