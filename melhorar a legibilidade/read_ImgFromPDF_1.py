#pip install PyPDF2
import PyPDF2
from PIL import Image
from PyPDF2 import PdfReader


if __name__ == '__main__':
    reader = PdfReader(open("english-in-common-5.pdf", "rb"))
    number_of_pages = len(reader.pages)

    for i in range(0, number_of_pages):
        page = reader.pages[i]
        xObject = page['/Resources']['/XObject'].get_object()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject [obj]['/Width'], xObject [obj]['/Height'])
                data = xObject [obj].get_data() 
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"

                if xObject [obj] ['/Filter' ] == '/FlateDecode':
                    img = Image.frombytes (mode, size, data) 
                    img.save("original_pages\\" + obj[1:] + ".png")
                elif xObject [obj]['/Filter'] == '/DCTDecode':
                    img = open ("original_pages\\" + obj [1:] + ".jpg", "wb")
                    img.write (data)
                    img.close()
                elif xObject[obj]['/Filter' ] == '/JPXDecode' :
                    img = open ("original_pages\\" + obj[1:] + ".jp2", "wd")
                    img.write (data)
                    img.close ()



# def setOriginalPdfFileName(self, name):
#     originalFileName = name

# def getOriginalPdfFileName():
#     return originalFileName 

