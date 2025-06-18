import json
import pandas as pd
from docx import Document
from pathlib import Path

def parse_file(file_path: Path) -> str:
    """
    Auto-detect and parse the uploaded file based on extension.
    Returns a clean string that summarizes key info.
    """
    ext = file_path.suffix.lower()

    if ext == ".jsonld":
        return parse_jsonld(file_path)
    elif ext == ".csv":
        return parse_csv(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    else:
        return f"Unsupported file type: {ext}"

def parse_jsonld(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        entries = data.get("@graph", []) if "@graph" in data else [data]
    elif isinstance(data, list):
        entries = data
    else:
        return "Unrecognized JSON-LD format."

    extracted = []

    for entry in entries:
        facets = entry.get("uco-core:hasFacet", [])
        if not isinstance(facets, list):
            facets = [facets]

        for facet in facets:
            facet_type = facet.get("@type")
            if facet_type == "uco-observable:EventRecordFacet":
                record_id = facet.get("uco-observable:eventRecordID", "UnknownID")
                event_type = facet.get("uco-observable:eventType", "UnknownType")
                timestamp = facet.get("uco-observable:startTime", {}).get("@value", "UnknownTime")

                extracted.append(
                    f"EventRecordID: {record_id}, Timestamp: {timestamp}, Type: {event_type}"
                )

    if len(extracted) <= 40:
        return "\n".join(extracted)
    else:
        # Get first 10 and last 10 entries
        # return "\n".join(extracted)
        return "\n".join(extracted[:10] + ["... (omitted) ..."] + extracted[-10:])




def parse_csv(path: Path) -> str:
    df = pd.read_csv(path)
    preview = df.head(10).to_string(index=False)
    return f"CSV Preview:\n{preview}"

def parse_docx(path: Path) -> str:
    doc = Document(path)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return f"Extracted DOCX Text (first 1000 chars):\n{text[:1000]}"