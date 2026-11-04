FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir \
    fastapi==0.115.5 \
    uvicorn[standard]==0.32.0 \
    jinja2==3.1.4 \
    python-multipart==0.0.17 \
    pillow==11.0.0 \
    torch==2.5.1 \
    torchvision==0.20.1

COPY . .

RUN python -c "from torchvision import models; models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT); print('Model loaded successfully')"

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]