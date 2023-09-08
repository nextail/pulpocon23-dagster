from dagster import build_op_context

from pulpocon23_dagster.chapter_1.op_graph_job import add_numbers

context = build_op_context()


def test_add_numbers():
    assert add_numbers(context, num1=1, num2=2) == 3
