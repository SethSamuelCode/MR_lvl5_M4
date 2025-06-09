FROM python:3.12-alpine 

COPY . /app/back
WORKDIR /app/back

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Using uvicorn with proxy settings
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]