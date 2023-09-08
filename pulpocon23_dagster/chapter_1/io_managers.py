from dagster import asset


@asset(key_prefix=["examples"], group_name="io_manager", name="give_me_five_asset", io_manager_key="fs_io_manager")
def give_me_five_asset():
    return 5
