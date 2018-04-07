import yaml
import slack

with open('./config.yml', 'r') as f:
    config = yaml.load(f)


def lambda_handler(event, context):
    client = slack.SlackApiClient(config['slack'])
    client.delete_expired_files()


if __name__ == '__main__':
    lambda_handler('hoge', 'fuga')
