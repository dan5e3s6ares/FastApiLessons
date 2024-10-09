# FastApiLessons
Passo a passo de criação de um servidor em FastAPi, os passos estão separados por branch

## Hello World
- Step 1:
    > Create & Activate Python Env
    ```shell
    foo@bar:~$ python3 -m venv .env

    foo@bar:~$ source .env/bin/activate
    ```
    > Install dependencies
    ```bash
    foo@bar:~$ pip install "fastapi[standard]"
    ```
- Step 2:
    > Create main.py file
    ```shell
    touch main.py
    ```
- Step 2:
    > Type your first code with one endpoint
    ```python
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    ```