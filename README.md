## Event Driven Notifications Platform
A unified, reliable mechanism for delivering user notifications from across different services with minimum latency

### REST API DESIGN
Example design for one of the API's `/preferences`
![rest_api_design_example](rest_api.jpg)

#### AUTHENTICATION DESIGN FOR MAKING THE ENDPOINTS PROTECTED
    
- I have used `python-jose` lib as the authentication provider and Redis as the centralized credentials store
- So to verify this flow the first step is to make a POST http://localhost:8000/api/v1/auth/login with a 
{username:str, password:str} passed in the request body
- If the username and password is of a valid existing user then 
`def create_access_token()` will generate a bearer access token
- Then the `def get_current_user()` will decode that token and return the authenticated user which will be used via dependency injection in all API requests


### TECH STACK

- FastAPI for building REST Endpoints
- Python Jose for basic jwt based auth identity provider
- Redis as a credential store
- AWS DynamoDB as the data store
- Kafka as event streaming messaging system
- #TODO: Add more as we develop



### How to start the App

- Prereq: Python 3.11 or greater is installed
- Clone the project & cd into the root directory 
- Make sure you have a `.env` file created with all the required AUTH0 and other env vars
- Run `python -m pip install --upgrade pip`
- Run `pip install -r requirements.txt`
- Make sure `Docker` is installed and a redis client is running in your local via `docker run -p 6379:6379 -it redis:latest`
- Run `uvicorn main:app --reload`
- To close the app `CTRL+C`


### Linting and Formatting
RUN 
```bash
Linting:
pylint "path to module/directory" OR 
ruff check "path to module/directory"

Formatting:
black "path to module/directory"
```


### TODO: Explain the Project structure and flow 
### TODO: Explain how to test?