import pymupdf

doc = pymupdf.open("progres_robotika.pdf")
for i in [0, 5, 6, 7, 8, 9]:
    page = doc[i]
    pix = page.get_pixmap(dpi=150)
    pix.save(f"page_{i+1}.png")
print("saved")
