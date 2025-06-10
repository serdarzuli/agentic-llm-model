# tools/image_parser.py

from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration  # Model bileşenleri
from PIL import Image  # Görsel işlemleri için
from pathlib import Path
import torch

# Model and processor loading
processor = Pix2StructProcessor.from_pretrained("google/pix2struct-base")
model = Pix2StructForConditionalGeneration.from_pretrained("google/pix2struct-base")

def parse_image_structure(image, image_name="uploaded_image"):
    """
    image_name: File name or a unique name
    """
    inputs = processor(images=image, return_tensors="pt")  # Convert to tensor
    with torch.no_grad():  # Work in inference mode
        outputs = model.generate(**inputs, max_length=512)  # Generate the response

    result = processor.decode(outputs[0], skip_special_tokens=True)  # Get the text

    return {
        "text": result.strip(),            # Extracted content
        "source_id": image_name,      # File name
        "title": Path(image_name).stem,          # File name without extension
        "type": "image_structured_data"    # Content type
    }

def parse_all_images(folder_path):
    """
    Processes all images in the specified folder.
    """
    folder = Path(folder_path)
    supported_ext = [".jpg", ".jpeg", ".png", ".bmp"]
    all_parsed = []

    for image_file in folder.glob("*"):
        if image_file.suffix.lower() in supported_ext:
            parsed = parse_image_structure(image_file)
            all_parsed.append(parsed)

    return all_parsed
