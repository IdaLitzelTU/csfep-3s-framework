"""internal kitchen to dynamically import models"""

import os

dir = os.path.dirname(os.path.abspath("client/client"))
# extract file names that start with letter v
modules = [
    os.path.splitext(_file)[0] for _file in os.listdir(dir) if _file.startswith("v")
]

client = []
for mod in modules:
    # imports all model version files from the folder and appends them to a list
    exec("from client import {}; client.append({})".format(mod, mod))


def model_versions(modules, client):
    """
    This function iterates through the model version files found in the client folder
    and returns a dictionary with the module attributes of each version like below:

    model_export = {
    "v1": {
        "exec": v1.run,
        "meta": v1.meta,
        "input": v1.input,
        "params":v1.params
        },
    }

    """
    model_export = {}
    for index, mod in enumerate(modules):
        model_export[mod] = {
            "exec": client[index].run,
            "meta": client[index].meta,
            "input": client[index].input,
            "params": client[index].params,
            "assumptions": client[index].assumptions,
        }

    return model_export


model_export = model_versions(modules, client)
