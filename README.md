# Pet Breed Identifier

## Overview

Pet Breed Identifier is a lightweight FastAPI web application that performs image-based pet breed estimation using a pretrained MobileNetV2 model from TorchVision.

Features:

- Image upload
- Instant image preview
- FastAPI backend
- Top-5 prediction results
- CPU-friendly inference
- Error handling
- Disclaimer that predictions are estimates

## Requirements

- Python 3.10+
- Internet connection on first run for model download

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Model Preparation

The application uses TorchVision's pretrained MobileNetV2 model.

On first startup TorchVision may automatically download pretrained weights.

No manual model download is required.

## Run

Start the server:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

## API Endpoint

POST:

```text
/predict
```

Form field:

```text
file
```

Supported formats:

- JPG
- JPEG
- PNG

## Disclaimer

This application provides estimated predictions only and should not be considered professional breed identification.
