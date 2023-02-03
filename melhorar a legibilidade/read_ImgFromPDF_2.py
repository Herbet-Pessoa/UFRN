#pip install fitz
import fitz

doc = fitz.open("english-in-common-5.pdf")

for i in range(len(doc)):
    for img in doc.getPageImageList(i):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n < 5:     #this is GRAY or RGB
            pix1.writePNG("p%s-%s.png" % (i, xref))
        else:
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            pix1.writePNG("p%s-%s.png" % (i, xref))
            pix1 =  None
        pix = None