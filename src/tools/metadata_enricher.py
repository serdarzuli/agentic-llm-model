from datetime import datetime
from pathlib import Path

def enrich_metadata(item, extra_meta=None):
    """
    Enriches a single piece of content with standard metadata fields.

    item: {
        'text': '...',
        'source_id': 'file.pdf',
        'type': 'pdf',
        ...
    }
    extra_meta: Optional additional metadata like {'date': ..., 'page': ..., 'speaker': ...}
    """
    enriched = {
        "text": item.get("text", "").strip(),                       # Main content (text)
        "source_id": item.get("source_id", "unknown"),              # File name or ID
        "title": item.get("title", item.get("source_id", "")).replace("_", " ").split(".")[0],  # Title
        "type": item.get("type", "unknown"),                        # Resource type (pdf, audio, image, etc.)
        "date": item.get("date", "").strip(),                       # Date (if available)
        "page": item.get("page", 1),                                # Page number (if available)
    }

    # Add optional fields (e.g., page, speaker, project, etc.)
    if extra_meta:
        enriched.update(extra_meta)

    return enriched

def enrich_batch(items, default_meta=None):
    """
    Batch metadata enrichment for multiple chunks.
    """
    return [enrich_metadata(item, default_meta) for item in items]
