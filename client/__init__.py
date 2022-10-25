# internal kitchen to import models
import client.v1 as v1

model_export = {
    "v1": {
        "exec": v1.run,
        "meta": v1.meta,
        "input": v1.input,
    }
}
