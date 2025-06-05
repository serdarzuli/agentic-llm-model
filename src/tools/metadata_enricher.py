# tools/metadata_enricher.py

from datetime import datetime
from pathlib import Path

def enrich_metadata(item, extra_meta=None):
    """
    Tek bir içerik parçasına standart metadata alanlarını ekler.

    item: {
        'text': '...',
        'source_id': 'file.pdf',
        'type': 'pdf',
        ...
    }
    extra_meta: {'date': ..., 'page': ..., 'speaker': ...} gibi opsiyonel değerler
    """
    enriched = {
        "text": item.get("text", "").strip(),                       # Ana içerik (metin)
        "source_id": item.get("source_id", "unknown"),              # Dosya adı veya ID
        "title": item.get("title", item.get("source_id", "")).replace("_", " ").split(".")[0],  # Başlık
        "type": item.get("type", "unknown"),                        # Kaynak türü (pdf, audio, image, vs.)
        "date": item.get("date", "").strip(),                       # Tarih (varsa)
        "page": item.get("page", 1),                                # Sayfa numarası (varsa)
    }

    # Opsiyonel alanlar ekleniyor (örneğin sayfa, konuşmacı, proje vs.)
    if extra_meta:
        enriched.update(extra_meta)

    return enriched

def enrich_batch(items, default_meta=None):
    """
    Birden fazla chunk için batch metadata zenginleştirme.
    """
    return [enrich_metadata(item, default_meta) for item in items]
