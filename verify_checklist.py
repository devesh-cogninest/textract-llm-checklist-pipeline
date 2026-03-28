from checklist_from_excel import load_excel_checks, filter_checks_by_doc_type
from ocr_checklist_generator import extract_values, build_ocr_checklist
from ocr_module import detect_document_type, call_llm


EXCEL_PATH = "Verification_Checks_Summary_Shared.xlsx"
OCR_FILE = "ocr_text.txt"

VALID_TYPES = ["Letter of Credit", "Bill of Lading", "Commercial Invoice"]


# Load OCR text
with open(OCR_FILE, "r", encoding="utf-8") as f:
    ocr_text = f.read()


# Detect document type
doc_type = detect_document_type(ocr_text, VALID_TYPES)
print(f"Detected Document Type: {doc_type}\n")


# --- EXCEL CHECKLIST ---
all_checks = load_excel_checks(EXCEL_PATH)
filtered_checks = filter_checks_by_doc_type(all_checks, doc_type)
excel_names = [c["check_name"] for c in filtered_checks]


# --- LC CHECKLIST (from OCR + LLM) ---
extracted_values = extract_values(filtered_checks, ocr_text, call_llm)
lc_checklist = build_ocr_checklist(filtered_checks, extracted_values)
lc_names = [c["check_name"] for c in lc_checklist]


# --- COMPARISON ---
excel_set = set(excel_names)
lc_set = set(lc_names)

missing_in_lc = excel_set - lc_set
extra_in_lc = lc_set - excel_set
null_values = [c["check_name"] for c in lc_checklist if c["value"] is None]
found_values = [c["check_name"] for c in lc_checklist if c["value"] is not None]


print("=" * 60)
print("         CHECKLIST VERIFICATION REPORT")
print("=" * 60)

print(f"\nTotal Excel checks (filtered): {len(excel_names)}")
print(f"Total LC checks:               {len(lc_names)}")

print(f"\n--- Checks in Excel but MISSING in LC ---")
if missing_in_lc:
    for name in sorted(missing_in_lc):
        print(f"  ✗ {name}")
else:
    print("  None — all Excel checks are present in LC checklist")

print(f"\n--- Extra checks in LC not in Excel ---")
if extra_in_lc:
    for name in sorted(extra_in_lc):
        print(f"  ? {name}")
else:
    print("  None")

print(f"\n--- Checks with NULL values (not found in document) ---")
if null_values:
    for name in null_values:
        print(f"  ✗ {name}")
else:
    print("  None — all checks have extracted values")

print(f"\n--- Checks with extracted values ---")
for name in found_values:
    val = extracted_values.get(name)
    print(f"  ✓ {name}: {val}")

print(f"\n{'=' * 60}")
print(f"SUMMARY: {len(found_values)}/{len(excel_names)} checks have values, "
      f"{len(null_values)} null, {len(missing_in_lc)} missing")
print(f"{'=' * 60}")
