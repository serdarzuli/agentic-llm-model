# tools/image_parser.py

from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration  # Model bileşenleri
from PIL import Image  # Görsel işlemleri için
from pathlib import Path
import torch

# Model ve işlemci yükleniyor
processor = Pix2StructProcessor.from_pretrained("google/pix2struct-base")
model = Pix2StructForConditionalGeneration.from_pretrained("google/pix2struct-base")

def parse_image_structure(image_path):
    """
    Tek bir görseldeki yapılandırılmış içeriği (form, tablo, diyagram) çözümler.
    """
    image = Image.open(image_path).convert("RGB")  # Görseli RGB olarak aç

    inputs = processor(images=image, return_tensors="pt")  # Tensöre dönüştür
    with torch.no_grad():  # Inference modunda çalış
        outputs = model.generate(**inputs, max_length=512)  # Cevabı üret

    result = processor.decode(outputs[0], skip_special_tokens=True)  # Metni al

    return {
        "text": result.strip(),            # Çıkarılan içerik
        "source_id": image_path.name,      # Dosya adı
        "title": image_path.stem,          # Uzantısız dosya adı
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
