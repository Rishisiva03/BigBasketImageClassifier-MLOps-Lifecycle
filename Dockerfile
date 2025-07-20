
FROM python:3.10-slim


WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY assets/ ./assets/
COPY notebooks/ ./notebooks/
COPY mlruns/ ./mlruns/

EXPOSE 8000

CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.port=8000"]
