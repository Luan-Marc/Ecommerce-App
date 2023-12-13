# Projeto E-commerce

O projeto E-commerce é uma aplicação web desenvolvida em Django, um framework poderoso para construção de aplicações web em Python.

## Configuração e Execução

Siga as instruções detalhadas abaixo para configurar o projeto em seu ambiente local.

### Pré-requisitos

- Python 3.x instalado em sua máquina
- Virtualenv instalado (`pip install virtualenv`)

### Instalação

1. **Crie um ambiente virtual:**

    ```bash
    virtualenv ecommerce
    ```

2. **Ative o ambiente virtual:**

    - No Windows:

        ```bash
        .\ecommerce\Scripts\activate
        ```

    - No Unix ou MacOS:

        ```bash
        source ecommerce/bin/activate
        ```

3. **Navegue até o diretório do projeto:**

    ```bash
    cd ecommerce
    ```

4. **Clone o repositório dentro do ambiente virtual:**

    ```bash
    git clone https://github.com/Luan-Marc/ecommerce-app.git
    ```

5. **Navegue até o diretório do projeto clonado:**

    ```bash
    cd ecommerce-app
    ```

6. **Instale as dependências do projeto:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuração do Banco de Dados

1. **Aplique as migrações do banco de dados:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Configuração do Crispy Forms

1. O Crispy Forms está configurado com o Bootstrap 5. Ajuste as configurações `CRISPY_ALLOWED_TEMPLATE_PACKS` e `CRISPY_TEMPLATE_PACK` em `settings.py` se necessário.

### Configuração do Número de Telefone

1. A região padrão para números de telefone está configurada como 'BR' (Brasil). Ajuste `PHONENUMBER_DEFAULT_REGION` em `settings.py` para uma região diferente.

### Executar a Aplicação

1. **Inicie o servidor de desenvolvimento:**

    ```bash
    python manage.py runserver
    ```

2. Abra seu navegador e acesse [http://127.0.0.1:8000/](http://127.0.0.1:8000/) para utilizar a aplicação.

## Conclusão

Você configurou e instalou com sucesso o projeto E-commerce. Explore a aplicação e personalize-a conforme suas necessidades. Se encontrar problemas, consulte a [documentação do Django](https://docs.djangoproject.com/) para obter ajuda.
