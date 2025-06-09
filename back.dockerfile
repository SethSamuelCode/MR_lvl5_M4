FROM python:3.12-alpine 

COPY . /app/back
WORKDIR /app/back

RUN pip install --no-cache-dir --upgrade -r requirements.txt



ENTRYPOINT ["fastapi","run","server.py"]