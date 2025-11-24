from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io
import uvicorn

app = FastAPI(title="Tesseract OCR API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Tesseract OCR API is running", "endpoint": "/ocr"}

@app.post("/ocr")
async def extract_text(
    file: UploadFile = File(...),
    lang: str = "eng"
):
    """
    Extract text from an uploaded image using Tesseract OCR.
    
    Parameters:
    - file: Image file (PNG, JPG, JPEG, etc.)
    - lang: Language code (default: 'eng' for English)
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )
    
    try:
        # Read image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Perform OCR
        text = pytesseract.image_to_string(image, lang=lang)
        
        # Get additional information
        data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
        valid = [c for c in data['conf'] if c != -1]
        
        return JSONResponse(content={
            "filename": file.filename,
            "text": text,
            "language": lang,
            "confidence": sum(valid) / len(valid) if valid else 0
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    