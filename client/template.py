""" Template on the structure of a model version file"""

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

params = {
    # dictionary for the parameter values
}


def run(data, params, *args, **kwargs):
    """
    This function runs the model with given inputs and returns results in JSON format


    The output of this method is directly fed into the frontend of the application. To make sure
    backwards compatibility, please make sure you are returning an object with the following structure:

     output = {
        "tC": {"constants": {}, scenario_{x: 1|2|3}: {} }, # the output in Carbon (T)
        "tCO2": {"constants": {}, scenario_{x: 1|2|3}: {} }, # the output in Carbon Dioxide (T)
        "assumtions": {}
    }

    Variables that the frontend displays are as follows:

    Constants:
        "Accumulated"
        "Harvested"
        "Buildings floor area m2"
        "Number of Buildings"
        "Years to Regrow Forest"

    Scenario variables:
        Carbon Recovered during Building Lifetime
        C2Scrap
        C2Forest
        C2Buildings

        MT Production
        SC Production
        MT Transport
        SC Transport

    Guidelines:
        If you want to consider Scrap or Forest as part of the Substitution or not at all, set variables
        C2Scrap, C2Forest to 0 and add the values to MT variables instead.

    Don't forget to adjust your assumtions!

    """
    pass
