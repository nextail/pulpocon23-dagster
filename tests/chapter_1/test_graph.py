from pulpocon23_dagster.chapter_1.examples.op_graph_job import math_operations

config = {
    "ops": {"add_numbers": {"inputs": {"num1": 1, "num2": 2}}, "add_numbers_2": {"inputs": {"num1": 1, "num2": 2}}}
}


def test_math_operations():
    result = math_operations.execute_in_process(run_config=config)
    assert result.success
