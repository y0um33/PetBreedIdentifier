from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import io
import torch
from torchvision import models, transforms

app = FastAPI(title="Pet Breed Identifier")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

weights = models.MobileNet_V2_Weights.DEFAULT
model = models.mobilenet_v2(weights=weights)
model.eval()

labels = weights.meta["categories"]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed"
        )

    try:
        content = await file.read()

        image = Image.open(
            io.BytesIO(content)
        ).convert("RGB")

        tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(tensor)
            probabilities = torch.nn.functional.softmax(
                output[0],
                dim=0
            )

        top_probs, top_indices = torch.topk(
            probabilities,
            5
        )

        predictions = []

        for prob, idx in zip(
            top_probs.tolist(),
            top_indices.tolist()
        ):
            predictions.append({
                "label": labels[idx],
                "confidence": round(prob * 100, 2)
            })

        return JSONResponse({
            "success": True,
            "disclaimer": (
                "Results are estimates only and may be inaccurate."
            ),
            "predictions": predictions
        })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )