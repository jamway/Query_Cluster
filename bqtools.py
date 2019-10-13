from google.cloud import bigquery, logging, pubsub
import pandas
from google.oauth2 import service_account
import json

class bqclient:
    def __init__(self, path_to_cred, project_id):

        self.credentials = service_account.Credentials.from_service_account_file(path_to_cred)
        self.project_id = project_id
        self.queryclient = bigquery.Client(credentials= self.credentials,project=project_id)
        self.logclient = logging.Client(credentials= self.credentials,project=project_id)
        self.pubsubclient = pubsub.PublisherClient(credentials=self.credentials)

    def query_data(self, query, use_legacy_sql=False):
        """Return query result as pandas dataframe"""
        job_config = bigquery.QueryJobConfig()
        job_config.use_legacy_sql = use_legacy_sql
        return self.queryclient.query(query, job_config=job_config).to_dataframe()
    
    def write_dataframe(self, dataframe, dataset_id, table_id, status, last_valid_date='' ):
        # replace with your table ID
        if os.environ["GLOBAL_LCP"] == "pr":
            ssr_project = ""
            cred = './credentials.json'
        else:
            ssr_project = ""
            cred = './credentials.json'
        client = bigquery.Client(credentials=cred, project_id = ssr_project)
        table_ref = client.dataset( ssr_project, dataset_id=dataset_id).table(table_id)
        try:
            table = client.get_table(table_ref)  # API request
            return self.query_client.load_table_from_dataframe(df, table_ref )
        except Exception as e:
            return e




    def write_entry(self, message):
        """Writes log entries to the given logger."""
    # This log can be found in the Cloud Logging console under 'Custom Logs'.
        logger = self.logclient.logger("Wei")

        # Make a simple text log
        logger.log_struct(message, severity='INFO')

    def publish_message(self, message, TOPIC):
        ## TODO: Decide TOPIC_STRING base on project
        TOPIC_STRING =f'projects/{self.project_id}/topics/{TOPIC}'
        print(TOPIC_STRING)
        self.write_entry(message)
        project_id = self.project_id
        future = self.pubsubclient.publish(
            TOPIC_STRING.format(project=project_id),
            json.dumps(message, ensure_ascii=False).encode('gbk'))
        message_id = future.result()
        print('Status output with message_id :: %s' % message_id)
        