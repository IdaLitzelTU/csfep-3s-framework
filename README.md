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
1. Client folder - Contains the versions of the model. Every version should be stored in a different file inside the folder following the template.py file structure.  
2. Framework folder - Contains file csfep_3s.py which has the functions implemented in the model version files.   

3. app.py  
This is the main file that contains the project api. It has 2 endpoints:
    > /model  
    > /dataset


**To get all model versions:**  
Use GET method on 
```
server_location/model

Example:
"http://127.0.0.1:8000/model"

```

**To get a specified model version information:**  
Use GET method on
```
server_location/model/model_version

Example:
"http://127.0.0.1:8000/model/v1"
```

**To run a specified model version and return the output:**    
Use POST method on
```
server_location/model/model_version

Example:
"http://127.0.0.1:8000/model/v1"
```
