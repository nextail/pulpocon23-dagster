from dagster import asset


@asset(io_manager_key="fs_io_manager")
def give_me_five_asset():
    return 5
