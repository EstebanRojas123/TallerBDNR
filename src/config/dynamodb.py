import boto3 

# Configurar DynamoDB Local
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',  
    region_name='us-west-2',
    aws_access_key_id='fakeAccessKeyId',  
    aws_secret_access_key='fakeSecretAccessKey'
)



