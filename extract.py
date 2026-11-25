import pymupdf

doc = pymupdf.open("progres_robotika.pdf")
print("PAGES:", doc.page_count)
out = []
for i, page in enumerate(doc):
    out.append(f"\n===== PAGE {i+1} =====\n")
    out.append(page.get_text())
with open("extracted.txt", "w", encoding="utf-8") as f:
    f.write("".join(out))
print("done")
