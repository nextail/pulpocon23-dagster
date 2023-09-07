from dagster import AssetExecutionContext, ConfigurableResource, asset


class CredentialsResource(ConfigurableResource):
    username: str
    password: str


@asset(
    key_prefix=["examples"],
    group_name="resources",
)
def recover_credentials_asset(context: AssetExecutionContext, credentials: CredentialsResource):
    user = credentials.username
    password = credentials.password
    context.log.debug(f"User:{user}, Pass:{password}")
