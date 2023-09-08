from dagster import Config, RunConfig, asset, job, op


class InputConfig(Config):
    name: str


@asset(key_prefix=["examples"], group_name="configuration", name="recover_name_asset")
def recover_name_asset(context, config: InputConfig) -> str:
    name = config.name
    context.log.debug(f"My name is: {name}")
    return name


@op
def recover_name_op(context, config: InputConfig) -> str:
    name = config.name
    context.log.debug(f"My name is: {name}")
    return name


recover_name_job_config = RunConfig({"recover_name_op": InputConfig(name="Alice")})


@job(config=recover_name_job_config)
def recover_name_job():
    recover_name_op()
