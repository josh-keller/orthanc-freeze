FROM python:3.9-slim

WORKDIR /app

RUN pip install pynetdicom

# Patch pynetdicom
COPY patch.txt .
RUN sed -i '/Try and get the first yield/r patch.txt' /usr/local/lib/python3.9/site-packages/pynetdicom/service_class.py
RUN sed -i '/from io import BytesIO/i\import time\n' /usr/local/lib/python3.9/site-packages/pynetdicom/service_class.py

COPY server.py .
CMD ["python", "server.py"]
