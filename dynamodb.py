import boto3
from botocore.exceptions import ClientError


class GreetingHandler:

    def __init__(self, table_name):
        try:
            db = boto3.resource('dynamodb')

            self.table = db.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'gid',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'gid',
                        'AttributeType': 'N'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                    }
            )

            self.table.meta.client.get_waiter('table_exists').wait(
                TableName=table_name)
        except ClientError:
            self.table = boto3.resource('dynamodb').Table(table_name)

    def add_greeting(self, gid, date, content):
        self.table.put_item(
            Item={'gid': gid,
                  'date': date,
                  'content': content}
        )
        return self.table.item_count

    def get_greeting(self, gid):
        return self.table.get_item(
            Key={'gid': gid}
        )['Item']

    def delete_greeting(self, gid):
        self.table.delete_item(
            Key={'gid': gid}
        )


if __name__ == "__main__":
    service = GreetingHandler('greetings')
