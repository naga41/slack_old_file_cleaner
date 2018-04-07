from datetime import datetime, timedelta

import boto3
from slackclient import SlackClient


class SlackApiClient:
    def __init__(self, config):
        self.config = config
        self.sc = SlackClient(self.get_slack_token())

    def delete_expired_files(self):
        expired_file_list = self.get_file_list(
            days_to=self.config['delete_file']['days_to_delete']
        )
        print('delete_target_file_count:', len(expired_file_list))
        for index, file in enumerate(expired_file_list):
            if self.delete_file(file['id']):
                print('#' + str((index + 1)) + ' DELETED:', file['title'])

    def delete_file(self, file_id):
        response = self.sc.api_call(
            "files.delete",
            file=file_id
        )
        return response['ok']

    def get_file_list(self, days_to=0, page=1):
        timestamp_to = (datetime.now() - timedelta(days=days_to)).strftime('%s')
        response = self.sc.api_call(
            "files.list",
            page=page,
            ts_to=timestamp_to,
            types=",".join(self.config['delete_file']['file_types'])
        )
        if self.get_next_page(response['paging']):
            additional_file_list = self.get_file_list(days_to=days_to, page=page + 1)
            response['files'].extend(additional_file_list)

        return response['files']

    def get_next_page(self, paging):
        return paging['pages'] > paging['page']

    def get_slack_token(self):
        client = boto3.client('ssm')
        response = client.get_parameter(
            Name=self.config['token']['ssm_param_name'],
            WithDecryption=True
        )
        return response['Parameter']['Value']
