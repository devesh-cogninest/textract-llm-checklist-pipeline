# textract-llm-checklist-pipeline

Problem :
Mera goal hai ki trade finance documents (LC, B/L, etc.) ke liye sirf relevant checks run karu instead of all 114 checks.
Iske liye pehle document type detect karta hoon, phir Excel se sirf us type ke applicable checks filter karta hoon, aur final JSON checklist generate karta hoon.

Cell 1–4: Setups
Isme maine required libraries install ki, imports kiye, AWS credentials set kiye aur Textract aur Bedrock clients initialize kiye.
Ye pura environment setup part hai.

Cell 5: Excel Load
Yahan maine Verification Excel file read ki aur har row ko dictionary format me list me store kiya.
Main column use kiya Col E (checked_against), jo batata hai ki kaunsa check kis document type pe apply hota hai.
Cash related checks (Col I = Cash) ko skip kiya kyunki wo required nahi the.

Cell 6: Filter Logic
Ye sabse important part hai.
Document type detect hone ke baad uske corresponding keywords define kiye.
Example: LC ke liye keywords ["LC", "Letter of Credit", "All documents"]
Phir Excel ke Col E me keyword match karke sirf relevant checks select kiye.
Col E use kiya kyunki ye batata hai ki check kis document type pe apply hota hai, jabki Col F batata hai ki check kis document ke andar perform karna hai.

Cell 7: OCR and Document Type Detection

OCR Function
PDF ko pehle images me convert kiya (PyMuPDF use karke).
Phir har image ko AWS Textract me diya aur text extract kiya.
Textract images pe better perform karta hai isliye direct PDF ke bajaye images use ki.

Document Type Detection Function
OCR text ke first 2000 characters liye aur LLM ko diye.
LLM ko predefined document types ki list di aur bola ki sirf ek exact type return kare.
Isse output consistent aur directly usable milta hai.

Cell 8: Run OCR
Folder ke saare PDF files read kiye aur har file pe OCR run kiya.
Output ek dictionary me store kiya jisme filename ke against pages aur unka text store hai.
Isse baar baar OCR run karne ki zarurat nahi padti aur cost/time save hota hai.

Cell 9: Checklist Generation
Har PDF ke liye pehle document type detect kiya (LLM use karke).
Phir filter logic apply karke relevant checks nikale (Python logic se).
Is pipeline me pehle document type ke basis pe checks filter hote hain (jaise LC ke liye 82 checks).
Uske baad un checks ko unki category ke according group kiya h
Har check ke paas ek category hoti hai (jaise BASIC TRADE INFO, SHIPPING DETAILS, etc.), usi basis pe grouping hoti hai.
Uske baad JSON structure generate kiya jisme document type, total checks aur saare checks included hain.
ase checklist genrate keri h 

Cell 10–12: Output and Save
Checklist ko notebook me readable format me print kiya.
Final JSON file ko save kiya (final_checklist.json).
Optional summary bhi print ki jisme categories aur sample checks show kiye.

Overall Flow
PDF input diya
Textract se OCR karke text nikala
LLM se document type detect kiya
Excel se relevant checks filter kiye
Final JSON checklist generate kiya
JSON file save kar di

Design Decisions
Textract use kiya kyunki ye scanned aur complex documents pe better kaam karta hai.
Document type detection ke liye LLM use kiya kyunki headers vary karte hain.
Checklist filtering ke liye Python logic use kiya kyunki ye fast aur deterministic hai
Col E use kiya filtering ke liye kyunki ye correct mapping deta hai document type ke saath.
JSON output use kiya kyunki ye machine-readable hai aur downstream systems me easily use ho sakta hai..
