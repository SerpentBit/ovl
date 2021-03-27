from behave import given, when, then
from tests.steps.conts import DEFAULT_IMAGE


@given("An image")
def step_impl(context):
    context.image = DEFAULT_IMAGE.copy()


@given("context")
def step_impl(context):
    context.a = 5


@when("context happened")
def step_impl(context):
    print(context.a)


@then("something")
def step_impl(context):
    print(type(context))

