FROM python:3.13-slim

WORKDIR /usr/src/app

RUN chown -R root:root /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && apt-get clean
    
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

