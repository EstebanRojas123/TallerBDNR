from config.dynamodb import dynamodb
from botocore.exceptions import ClientError

# Crear tabla Users
def create_users_table():
    try:
        table = dynamodb.create_table(
            TableName='Users',
            KeySchema=[
                {'AttributeName': 'username', 'KeyType': 'HASH'}  # Partition Key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'username', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        print("Tabla Users creada con éxito.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("La tabla Users ya existe.")
        else:
            raise

def create_user_courses_table():
    try:
        # Crear tabla UserCourses
        table = dynamodb.create_table(
            TableName='UserCourses',
            KeySchema=[
                {'AttributeName': 'username', 'KeyType': 'HASH'},  # Partition Key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'username', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        print("Tabla 'UserCourses' creada con éxito.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("La tabla 'UserCourses' ya existe.")
        else:
            print(f"Error al crear la tabla: {e}")

            raise

if __name__ == "__main__":
    create_users_table()
    create_user_courses_table()
