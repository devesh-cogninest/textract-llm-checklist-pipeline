import fitz, io, json
from PIL import Image
import boto3

from config import AWS_CONFIG

textract_client = boto3.client(
    "textract",
    region_name=AWS_CONFIG["region"],
    aws_access_key_id=AWS_CONFIG["access_key"],
    aws_secret_access_key=AWS_CONFIG["secret_key"]
)

bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_CONFIG["region"],
    aws_access_key_id=AWS_CONFIG["access_key"],
    aws_secret_access_key=AWS_CONFIG["secret_key"]
)


def call_llm(prompt, max_tokens=2048):
    body = json.dumps({
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {"maxTokens": max_tokens, "temperature": 0}
    })

    response = bedrock_client.invoke_model(
        modelId=AWS_CONFIG["model_id"],
        contentType="application/json",
        accept="application/json",
        body=body
    )

    return json.loads(response["body"].read().decode())["output"]["message"]["content"][0]["text"]


def pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []

    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        buf = io.BytesIO()
        img.save(buf, format="PNG")

        response = textract_client.analyze_document(
            Document={"Bytes": buf.getvalue()},
            FeatureTypes=["TABLES", "FORMS"]
        )

        text = "\n".join(
            b["Text"] for b in response["Blocks"] if b["BlockType"] == "LINE"
        )
        full_text.append(text)

    return "\n".join(full_text)


def detect_document_type(ocr_text, valid_types):
    prompt = f"""
Identify document type from below text.
Return ONLY one value from:
{valid_types}

Text:
{ocr_text[:2000]}
"""

    result = call_llm(prompt, max_tokens=50)

    for t in valid_types:
        if t.lower() in result.lower():
            return t

    return "Unknown"