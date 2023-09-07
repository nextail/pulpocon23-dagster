from dagster import graph, job, op


@op
def add_numbers(context, num1: int, num2: int) -> int:
    result = num1 + num2
    context.log.info(f"Adding {num1} + {num2} = {result}")
    return result


@op
def multiply_by_two(context, number: int) -> int:
    result = number * 2
    context.log.info(f"Multiplying {number} by 2 = {result}")
    return result


@graph
def math_operations():
    multiplied = multiply_by_two(add_numbers())
    add_numbers(multiplied, add_numbers())


@job
def math_job():
    math_operations()
