# Middleware Simples de Limitação de Taxa

Esta aplicação é uma API desenvolvida em Flask com um middleware para implementar limitação de taxa (rate limiting). O middleware controla o número de requisições permitidas por endereço IP dentro de uma janela de tempo configurável, retornando uma resposta apropriada se o limite for excedido.

---

## Passos para Executar a Aplicação

1. **Crie um Ambiente Virtual**

   - No diretório do projeto, crie um ambiente virtual:
     ```bash
     python -m venv venv
     ```
   - Ative o ambiente virtual:
     - **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     - **Linux/Mac**:
       ```bash
       source venv/bin/activate
       ```

2. **Crie o arquivo `.env`**

   - Na raiz do projeto, crie um arquivo chamado `.env`.
   - Adicione a seguinte variável:
     ```env
     SECRET_KEY=sua_chave_secreta_aqui
     ```

3. **Instale os Pacotes Necessários**

   - Certifique-se de estar com o ambiente virtual ativado.
   - Instale os pacotes listados no arquivo `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

4. **Execute a Aplicação**

   - No terminal, com o ambiente virtual ativado, execute o arquivo principal:
     ```bash
     python main.py
     ```
   - A aplicação será iniciada no endereço padrão: `http://127.0.0.1:5000`.

---

## Endpoints Disponíveis

### 1. **Configuração de Limites**

- **URL**: `/middleware/set_limits`
- **Método**: `POST`
- **Descrição**: Permite configurar os limites de taxa e a janela de tempo para o middleware.
- **Cabeçalho**:

  ```json
  Content-Type: application/json
  ```

- **Body (JSON)**:

```json
{
  "rate_limit": 10,
  "time_window": 60
}
```

- **Resposta de Sucesso (200)**:

```json
{
  "success": true,
  "message": "Rate limit set to 10 requests per 60 seconds."
}
```

- **Resposta de Erro (400 - Entradas Inválidas)**:

```json
{
  "success": false,
  "message": "Validations errors",
  "errors": {
    "rate_limit": ["'rate_limit' must be a valid integer."],
    "time_window": ["'time_window' must be a valid integer."]
  }
}
```

### 2. **API de Exemplo com Limitação de Taxa**

- **URL**: `/api/get_time`
- **Método**: `GET`
- **Descrição**:Retorna a data e hora atuais de Moçambique e Etiópia, com o middleware de limitação de taxa aplicado.

- **Resposta de Sucesso (200)**:

```json
{
  "success": true,
  "data": {
    "mozambique_time": "2025-01-15 15:30:00",
    "ethiopia_time": "2025-01-15 16:30:00"
  }
}
```

- **Resposta de Erro (429 - Limite de Taxa Excedido)**:

```json
{
  "success": false,
  "message": "Too Many Requests. Please try again later."
}
```

## Estrutura do Projeto

. ├── app/
│ ├── init.py
│ ├── configs.py
│ ├── middleware.py
│ ├── routes.py
│ └── validators.py
├── venv/
├── .env
├── main.py
├── requirements.txt
└── README.md

## Observações

- Certifique-se de que a variável `SECRET_KEY` está configurada no arquivo `.env` antes de executar a aplicação.
- Sempre ative o ambiente virtual antes de instalar os pacotes ou executar a aplicação:

  - **Windows**:
    ```bash
    venv\Scripts\activate
    ```
  - **Linux/Mac**:

    ```bash
    source venv/bin/activate
    ```

    ***

## Demonstração

- **Local**: `http://127.0.0.1:5000/`
- **Hospedado**: 
