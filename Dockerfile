# Budget Buddy container image

FROM python:3.13-slim

WORKDIR /app

COPY requirements-test.txt ./
RUN python -m pip install --no-cache-dir -r requirements-test.txt

COPY *.py ./
COPY data/ ./data/

CMD ["python", "main.py"]
