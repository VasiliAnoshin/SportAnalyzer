
# Sport Analyzer API

The Sport Analyzer API provides endpoints to retrieve information about sports games.

## Endpoints

### 1. List All Games

- **Endpoint:** `/list_all_games`
- **Method:** GET
- **Description:** Retrieve a list of all available sports games.
- **Example Request:**
  ```bash
  curl -X GET "http://localhost:8008/list_all_games"
  ```
  
- **Example Responce:**
  ```bash
    {
    "all_games": ["Volleyball", "Tennis", "Soccer", "Diagnostics", "EFootball", "TableTennis", "Basketball", "ESports", "Hockey", "Cricket", "Handball", "AmericanFootball", "Test"]
    }
  ```

### 2. List Total Games by Sport
- **Endpoint:** `/list_total_games_by_sport`
- **Method:** GET
- **Description:** Get the total number of games for a specific sport.
- **Parameters:**:
        - sport (query parameter): Filter games by sport.
- **Example Request:** 
  ```bash
  curl -X GET "http://localhost:8008/list_total_games_by_sport?sport=Tennis"
  ```

- **Example Responce:**
  ```bash
    {"Tennis": 150 }
  ```


## Docker
To run the Sport Analyzer API using Docker, follow these steps:
### 1. Build the Docker image:

        ```bash
        docker build -t my-fastapi-app .
        ```
### 2. Run the Docker container:
        ```bash
        docker run -p 8008:8008 my-fastapi-app
        ```
Now, the API is accessible at http://localhost:8008. You can use the provided endpoints as described above.

## Run SportAnalyzer in virtual environment

- Create virtual env:

```bash
        python -m virtualenv <folder_name>
```

- Create virtual environment version depend:

```bash
        virtualenv <folder_name> --python=python3.12
```

- activate

```bash
  .\<folder_name>\Scripts\activate.bat
```

- ctrl + shift + p: Python: Select interpreter
  should include Python interpreter related to your environment
- refresh terminal
- install requirements:
  There exist two requirements files one for production and one for development.

```bash
        pip install -r <Path_to_file>\requirements-dev.txt
```

- deactivate:

```bash
        deactivate
```
