from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT AS JSON 'auto'
        TIMEFORMAT AS 'epochmillisecs'
        region 'us-west-2'
    """

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 redshift_conn_id='',
                 aws_credentials_id='',
                 table='',
                 destination_table='',
                 s3_bucket="",
                 s3_key='',
                 delimiter=',',
                 ignore_headers=1,
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.destination_table = destination_table
        self.s3_bucket = s3_bucket
        self.key = key

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgress_conn_id=self.redshift_conn_id)
        self.log.info('StageToRedshiftOperator not implemented yet')

        redshift.run(f'DELETE FROM {self.table}')

        rendered_key = self.s3_key.format(**context)
        s3_path = 's3://{self.s3_bucket}/{rendered_key}'
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.ignore_headers,
            self.delimiter
        )
        redshift.run(formatted_sql)



