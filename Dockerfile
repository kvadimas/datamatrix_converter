FROM python:3.11-slim AS base
RUN apt update && apt -y install libdmtx0b && apt-get autoclean
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

FROM base
CMD ["python", "app.py"]