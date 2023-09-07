from dagster import RunConfig, materialize

from pulpocon23_dagster.chapter_1.examples.configuration import InputConfig, recover_name_asset


def test_asset_with_configuration():
    asset_result = materialize(
        [recover_name_asset],
        run_config=RunConfig({"examples__recover_name_asset": InputConfig(name="Alice")}),
    )
    assert asset_result.success
