meta = {
    "version": "1.0.1",  # version of the model
    "by": "some name",  # author's name
    "contact": "some.name@mail.com",  # author's email address
}

input = [
    # This list provides the metadata for the inputs. Each input variable is added to the list as a dictionary with the keys as described below.
    {
        "name": "",  # variable name of the input. Use the snake_case pattern for the name i.e, lowercase seperated by underscore symbol
        "category": "",  # category which the input variable falls under e.g. Forest, Manufacturing, Building
        "display_name": "",  # The display name of the input variable
        "description": "",  # A clear description statement of the variable
        "type": "",  # data type of the variable i.e. number, text, array of numbers (array[numbers])
        "default": "",  # the default value of the variable if any else indicate None
    },
]

model_parameters = {
    # dictionary for the parameter values
}


def run(data, params, *args, **kwargs):
    """
    This function runs the model with given inputs and returns results in JSON format
    """
    pass
