# CSFEP - 3S FRAMEWORK
##### (Climate Smart Forest Economy Program)  

This repo uses FastAPI and poetry as the dependency management tool.

## Installations
All dependencies are stored in the requirements.txt file. To install run: 
```python
    pip install -r requirements.txt
```


To use poetry for the installations run:
```python
pip install poetry
poetry shell  #Spawns a shell within the virtual environment
poetry install  #Installs the project dependencies
```

## How to run
In your terminal:
```
uvicorn app:app --reload
```

## Project structure
1. Client folder - Contains the versions of the model. Every version should be stored in a different file inside the folder following the template.py file structure and named with the version number e.g. for version 1: ***v1.py***

2. Framework folder - Contains file csfep_3s.py which has the functions implemented in the model version files.   

3. app.py  
This is the main file that contains the project api. It has 2 endpoints:
    > /model  
    > /dataset


**To get all model versions:**  
Use GET method on 
```
endpoint/model

Example:
"http://127.0.0.1:8000/model"

```

**To get a specified model version information:**  
Use GET method on
```
endpoint/model/model_version

Example:
"http://127.0.0.1:8000/model/v1"
```

**To run a specified model version and return the output:**    
Use POST method on
```
endpoint/model/model_version

Example:
"http://127.0.0.1:8000/model/v2"
```

### Adding a model version

To add a model version, create a version .py file in the client folder following the structure in the template.py file.  
The file is named by version number i.e. if the model is version 2 the file name would be ***v2.py***  

It should contain 4 attributes:  
1. **meta** - dictionary indicating the version of the model, name of the author and their contact.  
2. **input** - List of dictionaries, where each dictionary contains the metadata of an input variable. The keys of the dictionary should be name, category, display_name, description, type and default.

    ```python
    input = [
        {
            "name": "a_harvest", # variable name of the input.
            "category": "Forest", # category in which the input variable falls under e.g. Forest, Manufacturing, Building
            "display_name": "Harvested area (ha)", # The display name of the input variable
            "description": "An area of forest harvested in hectares", # A clear description statement of the variable
            "type": "number", # data type of the variable i.e. number, text, array of numbers (array[numbers])
            "default": "None", # the default value of the variable if any else indicate None
        },
    ]
    ```
3. **model_parameters** - dictionary of the parameter values
4. **run** function - function that runs the model with given data and returns results in JSON format
