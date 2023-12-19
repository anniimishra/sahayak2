import cv2
import easyocr
import re
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

# Function to extract text from an image using EasyOCR
def extract_text_from_image(contents):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(contents)
    text = ' '.join([entry[1] for entry in result])
    return text

# Function to extract name, DOB, and Aadhar number from the extracted text
def extract_info(text):
    # Assuming simple patterns for name, DOB, and Aadhar number extraction
    name_pattern = r"Name: ([A-Za-z ]+)"
    dob_pattern = r"DOB (\d{2}/\d{2}/\d{4})"
    aadhar_pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"

    name_match = re.search(name_pattern, text)
    dob_match = re.search(dob_pattern, text)
    aadhar_match = re.search(aadhar_pattern, text)

    name = name_match.group(1) if name_match else None
    dob = dob_match.group(1) if dob_match else None
    aadhar = aadhar_match.group() if aadhar_match else None

    return name, dob, aadhar

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    
    # Use EasyOCR to extract text from the image
    extracted_text = extract_text_from_image(contents)

    # Extract name, DOB, and Aadhar number from the text
    name, dob, aadhar = extract_info(extracted_text)

    # Return the results
    return {"filename": file.filename, "text": extracted_text, "name": name, "dob": dob, "aadhar": aadhar}
