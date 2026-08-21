FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#COPY nach /execute
COPY . .
EXPOSE 4300
#CMD = Command ohne extra shell
#kein "localhost" da externe anfrage
CMD ["uvicorn","server:app","--host","0.0.0.0","--port","4300"]