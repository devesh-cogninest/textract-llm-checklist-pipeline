import json
import re


def extract_values(fields, ocr_text, llm_func):
    field_names = [f['check_name'] for f in fields]

    prompt = f"""Extract exact values from the document text below.

Return a single JSON object where each key is a field name and the value is the extracted text (or null if not found).
Do not add any explanation — output only the JSON object.

Fields to extract:
{json.dumps(field_names, indent=2)}

Document text:
{ocr_text}
"""

    response = llm_func(prompt)

    # Strip markdown code fences if present
    clean = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.strip(), flags=re.DOTALL)

    try:
        parsed = json.loads(clean)
    except json.JSONDecodeError:
        return {}

    return parsed


def build_ocr_checklist(excel_checks, extracted):
    result = []

    for c in excel_checks:
        name = c["check_name"]

        result.append({
            "field_name": name,
            "check_name": name,
            "value": extracted.get(name),
            "match_type": c.get("rule"),
            "document_checked": c.get("document_checked")
        })

    return result