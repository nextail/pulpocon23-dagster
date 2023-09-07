from dagster import OpExecutionContext, job, op

from ..resources.postgres_resource import PostgresResource


@op
def introspect_tables(context: OpExecutionContext, postgres: PostgresResource):
    tables = postgres.query("SELECT * FROM pg_catalog.pg_tables")
    context.log.info(f"Got the following tables: #{tables}")


@job
def introspect_table_job():
    introspect_tables()
