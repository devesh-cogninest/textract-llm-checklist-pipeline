import zipfile, re
import xml.etree.ElementTree as ET


DOC_TYPE_KEYWORDS = {
    "Letter of Credit": ["LC", "Letter of Credit", "All"],
    "Bill of Lading": ["Bill of Lading", "B/L"],
    "Commercial Invoice": ["Invoice"]
}


def load_excel_checks(path):
    with zipfile.ZipFile(path) as z:
        ss = z.read("xl/sharedStrings.xml")
        sh = z.read("xl/worksheets/sheet1.xml")

    sh_root = ET.fromstring(sh)
    ss_root = ET.fromstring(ss)

    # Detect namespace dynamically from the root tag
    NS = sh_root.tag.split("}")[0].strip("{") if "}" in sh_root.tag else ""
    SS_NS = ss_root.tag.split("}")[0].strip("{") if "}" in ss_root.tag else ""

    def tag(ns, name):
        return f"{{{ns}}}{name}" if ns else name

    strings = [
        si.findtext(f".//{tag(SS_NS, 't')}") or ""
        for si in ss_root.findall(f".//{tag(SS_NS, 'si')}")
    ]

    rows = []
    for row in sh_root.findall(f".//{tag(NS, 'row')}"):
        data = {}
        for c in row.findall(tag(NS, "c")):
            col = "".join(filter(str.isalpha, c.get("r")))
            val = c.findtext(tag(NS, "v")) or ""
            if c.get("t") == "s" and val:
                val = strings[int(val)]
            data[col] = val
        rows.append(data)

    print("RAW EXCEL ROWS (first 5):")
    for r in rows[:5]:
        print(r)

    checks = []
    for r in rows[1:]:
        if not r.get("C"):
            continue

        checks.append({
            "check_name": r.get("C"),
            "checked_against": r.get("E"),
            "rule": r.get("G"),
            "document_checked": r.get("F")
        })

    return checks


def filter_checks_by_doc_type(checks, doc_type):
    keywords = DOC_TYPE_KEYWORDS.get(doc_type, [])

    return [
        c for c in checks
        if any(k.lower() in (c["checked_against"] or "").lower() for k in keywords)
    ]