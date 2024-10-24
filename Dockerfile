FROM python:3.10-slim
LABEL authors="r.shestov"

WORKDIR /fmsg-api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]