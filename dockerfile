FROM python:3.12-alpine 

COPY . /app/back
WORKDIR /app/back

RUN pip install --no-cache-dir -r requirements.txt



ENTRYPOINT ["fastapi","run","server.py"]