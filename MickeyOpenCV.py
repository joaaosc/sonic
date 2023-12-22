import cv2
from pdf2image import *
import fitz


# 'Primeira tentativa de ML: Viola-Jones algorithm #
# (https://en.wikipedia.org/wiki/Viola%E2%80%93Jones_object_detection_framework)'

pdf_path = r"DWGs/8200-DWG-BS-103-00.pdf"


def preprocess_image(image_path):
    """
    Processa uma imagem convertendo-a em escala de cinza e posteriormente aplicando binarização.
    Args:
        image_path (str): Caminho da imagem
    Returns:
        numpy.ndarray: Imagem binarizadaself.
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    print("~~sucessfully preproccessed")
    return binary_image


class pdfUtils:
    def __init__(self, pdfPath: str):
        self.pdfPath = pdfPath

    def get_table_of_contents(self):
        document = fitz.open(self.pdfPath)
        print(document.get_toc(), "aquii")

    def get_possible_drwaings(self):
        document = fitz.open(self.pdfPath)
        for page in document:

            print(page.bound().width, page.bound().height, f"aquiii{page.number}")

            if int(page.bound().width) > int(page.bound().height):
                pix = page.get_pixmap()  # render page to an image
                pix.save("page-%i.png" % page.number)  # store image as a PNG
                print("probably drawing found")
            else:
                print("probably not drawing")
                pass
        # end


# -------------------------------------------------------------------------------------------------#

instance = pdfUtils(pdf_path)
instance.get_possible_drwaings()
#  finish
