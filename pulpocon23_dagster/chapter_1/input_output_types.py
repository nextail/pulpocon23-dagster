from dagster import In, Int, Out, job, op


@op
def return_number() -> str:
    return "a"


@op(
    ins={"number_in": In(Int)},
    out={"numer_out": Out(Int)},
)
def add_one(number_in):
    number_out = number_in + 1
    return number_out


@job
def number_validation_job():
    add_one(return_number())
