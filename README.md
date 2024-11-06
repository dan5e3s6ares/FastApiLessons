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

## Path Parameters
Você pode declarar “parâmetros” ou “variáveis” de caminho com a mesma sintaxe usada pelas strings de formato do Python

- Step 1:
    > Update main.py - add items_any_type endpoint
    ```python
    ...
    @app.get("/items_any_type/{item_id}")
    async def read_item(item_id):
        return {"item_id": item_id}

    ```
- Step 2:
    > Update main.py - add items_integer endpoint
    ```python
    ...
    @app.get("/items_integer/{item_id}")
    async def read_item_integer(item_id : int):
        return {"item_id": item_id}
    ```
- Step 3:
    > Update main.py - add models endpoint with options
    ```python
    from enum import Enum
    ...
    class ItemsEnum(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"
    ...
    @app.get("/items_enum/{items_enum}")
    async def get_items_enum(items_enum: ItemsEnum):
        return {"Item Enum": items_enum}
    ```

## Query Parameters
Quando você declara outros parâmetros de função que não fazem parte dos parâmetros de caminho, eles são automaticamente interpretados como parâmetros de “consulta”.

- Step 1:
    > Update main.py
    ```python
    ...
    fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
    ...
    @app.get("/items/")
    async def read_query_items(skip: int = 0, limit: int = 10):
        return fake_items_db[skip : skip + limit]
    ```
    > [Consulta: http://127.0.0.1:8000/items/?skip=0&limit=1](http://127.0.0.1:8000/items/?skip=0&limit=1)

- Step 2:
    > Update main.py
    ```python
    ...
    @app.get("/items/{item_id}")
    async def read_item_optional(item_id: str, q: str | None = None):
        if q:
            return {"item_id": item_id, "q": q}
        return {"item_id": item_id}
    ```
    > [Consulta: http://127.0.0.1:8000/items/ABC?q=QWERTY](http://127.0.0.1:8000/items/ABC?q=QWERTY)
    > [Consulta: http://127.0.0.1:8000/items/ABC](http://127.0.0.1:8000/items/ABC)

## Request Body & PYDANTIC
Quando você precisa enviar dados de um cliente (digamos, um navegador) para a sua API, você os envia como um payload (request body).
Sua API quase sempre precisa enviar um payload de resposta. Mas os clientes não precisam necessariamente enviar payloads de solicitação o tempo todo, às vezes eles solicitam apenas um caminho, talvez com alguns parâmetros de consulta, mas não enviam um payload.
Para declarar um payload, você usa os modelos Pydantic com todo o seu poder e benefícios.

- Step 1:
    > Update main.py
    ```python
    ...
    from pydantic import BaseModel
    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None
    ...
    @app.post("/items/")
    async def create_item(item: Item):
        return item
    ```
    Requisição COM erros
    ```shell
    curl --location 'http://localhost:8000/items/' \
        --header 'Content-Type: application/json' \
        --data '{"abc":"ABC"}'
    ```
    Requisição SEM erros
    ```shell
    curl --location 'http://localhost:8000/items/' \
        --header 'Content-Type: application/json' \
        --data '{"name":"ABC", "price": 56.1}'
    ```
    Requisição SEM erros com todos os campos
    ```shell
    curl --location 'http://localhost:8000/items/' \
        --header 'Content-Type: application/json' \
        --data '{"name":"ABC", "description": "Descrição ","price": 56.1, "tax": 6.8}'
    ```
    Requisição COM erro com todos os campos
    ```shell
    curl --location 'http://localhost:8000/items/' \
        --header 'Content-Type: application/json' \
        --data '{"name":"ABC", "description": "Descrição ","price": 56.1, "tax": "ASD"}'
    ```

## Swagger OpenAPI

### Interactive API docs
Agora, acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Você verá a documentação interativa automática da API (fornecida pela Swagger UI)

### Alternative API docs
E agora, vá para [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Você verá a documentação automática alternativa (fornecida pelo ReDoc)

- Step 1:
    > Update main.py add tags
    ```python
    tags=["items"]
    tags=["items id"]
    tags=["items enum"]
    ```
- Step 2:
    > Update main.py
    ```python
    ...
    tags_metadata = [
        {
            "name": "items id",
            "description": "Operações com Items usando ID.",
        },
        {
            "name": "items",
            "description": "Operações Simples com Items",
        },
        {
            "name": "items enum",
            "description": "Operações com Items usando Enum de opções",
        },
    ]
    app = FastAPI(
        ...
        openapi_tags=tags_metadata,
    )
    ```
- Step 3
    > Update main.py add summary and description
    ```python
    ...
    @app.post(
        "/items/",
        tags=["items"],
        response_model=Item,
        summary="Create an Item",
        description="Create an Item with all the information",
    )
    ```
- Step 5
    > Update main.py add description with docstring
    ```python
    async def create_item(item: Item):
        """
        Create an item with all the information:

        - **name**: each item must have a name
        - **description**: a long description
        - **price**: required
        - **tax**: if the item doesn't have tax, you can omit this
        - **tags**: a set of unique tag strings for this item
        """
        ...
    ```

## Container - Docker

Os contêineres (principalmente os contêineres do Linux) são uma maneira muito leve de empacotar aplicativos,
incluindo todas as suas dependências e arquivos necessários, mantendo-os isolados de outros contêineres
(outros aplicativos ou componentes) no mesmo sistema.
</p>
Então, como rodar nosso servidor em um Container?
</p>

### Instalação do Docker e Docker Compose

#### Windows

1. **Baixar Docker Desktop:**
    - Acesse [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop) e baixe o instalador.

2. **Instalar Docker Desktop:**
    - Execute o instalador baixado e siga as instruções na tela.

3. **Verificar a instalação:**
    - Após a instalação, abra o terminal (PowerShell ou CMD) e execute:
    ```shell
    docker --version
    docker-compose --version
    ```

#### Linux (Ubuntu)

1. **Atualizar o índice de pacotes:**
    ```shell
    sudo apt-get update
    ```

2. **Instalar pacotes necessários:**
    ```shell
    sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    ```

3. **Adicionar a chave GPG oficial do Docker:**
    ```shell
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    ```

4. **Adicionar o repositório Docker:**
    ```shell
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

5. **Instalar Docker Engine:**
    ```shell
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

6. **Verificar a instalação do Docker:**
    ```shell
    sudo docker --version
    ```

7. **Instalar Docker Compose:**
    ```shell
    sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -Po '"tag_name": "\K.*\d')" /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```

8. **Verificar a instalação do Docker Compose:**
    ```shell
    docker-compose --version
    ```

9. **Adicionar o grupo docker**
    ```shell
    sudo groupadd docker
    ```

10. **Adicionar o usuário atual ao grupo docker**
    ```shell
    sudo gpasswd -a $USER docker
    ```

Agora você está pronto para rodar seu servidor FastAPI em um contêiner Docker!

### Rodando FastAPI com Docker Compose

#### Passo 1: Criar um arquivo `Dockerfile`
Crie um arquivo chamado `Dockerfile` no diretório raiz do seu projeto e adicione o seguinte conteúdo:

```dockerfile
# Use uma imagem base oficial do Python
FROM python:3.9

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de requisitos
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

#### Passo 2: Criar um arquivo `docker-compose.yml`
Crie um arquivo chamado `docker-compose.yml` no diretório raiz do seu projeto e adicione o seguinte conteúdo:

```yaml
version: '3.8'

services:
    web:
        build: .
        ports:
            - "8000:8000"
        volumes:
            - .:/app
        environment:
            - ENV=development
```

#### Passo 3: Criar um arquivo `requirements.txt`
Crie um arquivo chamado `requirements.txt` no diretório raiz do seu projeto e adicione as dependências do FastAPI:

```
fastapi
uvicorn[standard]
```

#### Passo 4: Rodar o Docker Compose
No terminal, navegue até o diretório raiz do seu projeto e execute o seguinte comando para iniciar o servidor FastAPI com Docker Compose:

```shell
docker-compose up --build
```

Agora, seu servidor FastAPI deve estar rodando em um contêiner Docker e acessível em [http://127.0.0.1:8000](http://127.0.0.1:8000).

## O que é o Banco de Dados Redis

Redis é um banco de dados de estrutura de dados em memória, usado como banco de dados, cache e broker de mensagens. Ele suporta estruturas de dados como strings, hashes, listas, conjuntos, conjuntos ordenados com consultas de intervalo, bitmaps, hiperloglogs, índices geoespaciais com consultas de raio e streams. Redis possui replicação integrada, scripts Lua, LRU eviction, transações e diferentes níveis de persistência no disco, além de alta disponibilidade e particionamento automático com Redis Sentinel e Redis Cluster.

Redis é conhecido por sua alta performance, simplicidade e flexibilidade, tornando-o uma escolha popular para aplicações que exigem respostas rápidas e armazenamento temporário de dados.

### Adicionando Redis ao Docker Compose

#### Passo 1: Atualizar o arquivo `docker-compose.yml`
Atualize o arquivo `docker-compose.yml` para incluir um serviço Redis:

```yaml
version: '3.8'

services:
    web:
        build: .
        ports:
            - "8000:8000"
        volumes:
            - .:/app
        environment:
            - ENV=development
        depends_on:
            - redis

    redis:
        image: "redis:alpine"
        ports:
            - "6379:6379"
```

#### Passo 2: Instalar a biblioteca Redis para Python
Adicione a biblioteca `redis` ao arquivo `requirements.txt`:

```
fastapi
uvicorn[standard]
redis
```

#### Passo 3: Atualizar o arquivo `main.py`
Atualize o arquivo `main.py` para incluir endpoints que permitem definir e buscar mensagens por ID:

```python
...
import redis

# Conectar ao Redis
r = redis.Redis(host='redis', port=6379, db=0)

class Payload(BaseModel):
    message: str
...

@app.post("/set_message/{message_id}")
async def set_message(message_id: str, payload: Payload):
    r.set(message_id, payload.message)
    return {"message": "Message set successfully", "id": message_id}

@app.get("/get_message/{message_id}")
async def get_message(message_id: str):
    message = r.get(message_id)
    if message:
        return {"message": message.decode('utf-8'), "id": message_id}
    return {"message": "No message found", "id": message_id}
```

#### Passo 2: Rodar o Docker Compose
No terminal, navegue até o diretório raiz do seu projeto e execute o seguinte comando para iniciar o servidor FastAPI e o Redis com Docker Compose:

```shell
docker-compose up --build
```

### Comandos curl para adicionar e consultar mensagens por ID

#### Adicionar uma mensagem por ID
```shell
curl --location --request POST 'http://127.0.0.1:8000/set_message/1' \
--header 'Content-Type: application/json' \
--data-raw '{"message":"Hello, Redis with ID!"}'
```

#### Consultar uma mensagem por ID
```shell
curl --location --request GET 'http://127.0.0.1:8000/get_message/1'
```
