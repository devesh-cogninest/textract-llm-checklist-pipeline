# from ocr_module import pdf_to_text, detect_document_type, call_llm
# from checklist_from_excel import load_excel_checks, filter_checks_by_doc_type
# from ocr_checklist_generator import extract_values, build_ocr_checklist

# EXCEL_PATH = "verification.xlsx"
# PDF_PATH = "lc.pdf"

# VALID_TYPES = ["Letter of Credit", "Bill of Lading", "Commercial Invoice"]


# # STEP 1: OCR
# ocr_text = pdf_to_text(PDF_PATH)

# # STEP 2: Detect Doc Type
# doc_type = detect_document_type(ocr_text, VALID_TYPES)
# print("Detected:", doc_type)

# # STEP 3: Excel Checklist
# all_checks = load_excel_checks(EXCEL_PATH)
# filtered_checks = filter_checks_by_doc_type(all_checks, doc_type)

# # STEP 4: Extract Values
# extracted = extract_values(filtered_checks, ocr_text, call_llm)

# # STEP 5: Final Checklist
# final_checklist = build_ocr_checklist(filtered_checks, extracted)

# print(final_checklist)

from checklist_from_excel import load_excel_checks, filter_checks_by_doc_type
from ocr_checklist_generator import extract_values, build_ocr_checklist
from ocr_module import detect_document_type, call_llm


EXCEL_PATH = `"Verification_Checks_Summary_Shared.xlsx"
OCR_FILE = "ocr_text.txt"

VALID_TYPES = ["Letter of Credit", "Bill of Lading", "Commercial Invoice"]


# STEP 1: Load OCR TEXT
with open(OCR_FILE, "r", encoding="utf-8") as f:
    ocr_text = f.read()

print("OCR Loaded [OK]")


# STEP 2: Detect Document Type
doc_type = detect_document_type(ocr_text, VALID_TYPES)
print("Detected Doc Type:", doc_type)


# STEP 3: Load Excel Checklist
all_checks = load_excel_checks(EXCEL_PATH)
filtered_checks = filter_checks_by_doc_type(all_checks, doc_type)

print(f"Filtered Checks: {len(filtered_checks)}")


# STEP 4: Extract Values using LLM
extracted_values = extract_values(filtered_checks, ocr_text, call_llm)


# STEP 5: Build Final Checklist
final_checklist = build_ocr_checklist(filtered_checks, extracted_values)


# OUTPUT
import json
print(json.dumps(final_checklist, indent=2))