import requests

def test_ocr(image_path: str, api_url: str = "http://localhost:8000/ocr"):
    try:
        with open(image_path, 'rb') as f:
            files = {
                'file': (image_path, f, 'image/png')
            }
            data = {
                'lang': 'eng'   # or 'spa', 'deu', etc.
            }
            response = requests.post(api_url, files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            print("OCR Result:")
            print(f"Filename: {result['filename']}")
            print(f"Language: {result['language']}")
            print(f"Confidence: {result['confidence']:.2f}%")
            print(f"\nExtracted Text:\n{result['text']}")
        else:
            print(f"Error: {response.status_code}")
            print(response.json())

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ocr("image.png")
