# Use uma imagem base do Python
FROM python:3.12

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para o container
COPY . /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Define o comando para rodar o Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]