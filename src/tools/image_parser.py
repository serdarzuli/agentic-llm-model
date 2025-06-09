# tools/image_parser.py

from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration  # Model bileşenleri
from PIL import Image  # Görsel işlemleri için
from pathlib import Path
import torch

# Model ve işlemci yükleniyor
processor = Pix2StructProcessor.from_pretrained("google/pix2struct-base")
model = Pix2StructForConditionalGeneration.from_pretrained("google/pix2struct-base")

def parse_image_structure(image, image_name="uploaded_image"):
    """
    image_name: Dosya adı veya benzersiz bir isim
    """
    inputs = processor(images=image, return_tensors="pt")  # Tensöre dönüştür
    with torch.no_grad():  # Inference modunda çalış
        outputs = model.generate(**inputs, max_length=512)  # Cevabı üret

    result = processor.decode(outputs[0], skip_special_tokens=True)  # Metni al

    return {
        "text": result.strip(),            # Çıkarılan içerik
        "source_id": image_name,      # Dosya adı
        "title": Path(image_name).stem,          # Uzantısız dosya adı
        "type": "image_structured_data"    # İçerik türü
    }

def parse_all_images(folder_path):
    """
    Belirtilen klasördeki tüm görselleri işler.
    """
    folder = Path(folder_path)
    supported_ext = [".jpg", ".jpeg", ".png", ".bmp"]
    all_parsed = []

    for image_file in folder.glob("*"):
        if image_file.suffix.lower() in supported_ext:
            parsed = parse_image_structure(image_file)
            all_parsed.append(parsed)

    return all_parsed
