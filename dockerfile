FROM python:3.12-slim
LABEL maintainer="https://github.com/gusteborges"

# Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependências de sistema (mínimo para buildar pacotes Python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python (antes de copiar o código para usar cache)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Criar usuário de segurança (não-root)
RUN useradd -m django-user && \
    chown -R django-user:django-user /app

# Copiar o projeto
COPY . .

# Mudar para o usuário seguro
USER django-user

EXPOSE 8000

# Comando para rodar a aplicação aceitando conexões externas
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]