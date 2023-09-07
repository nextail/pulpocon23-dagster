import psycopg2
from dagster import ConfigurableResource
from dagster_postgres.utils import get_conn_string


class PostgresResource(ConfigurableResource):
    hostname: str
    port: str
    username: str
    password: str
    db_name: str

    def query(self, sql: str):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    def execute(self, sql: str):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                return cur.execute(sql)

    def _get_connection(self):
        conn_str = get_conn_string(
            username=self.username,
            password=self.password,
            hostname=self.hostname,
            db_name=self.db_name,
            port=self.port,
        )
        return psycopg2.connect(conn_str)
