#  Copyright (C) 2023 João Pedro de S. T. Costa; read end of file for more information

import cv2
from pdfUtils import *

def main():
    instance = Pdfutils(pdf_path)
    drawings = instance.get_possible_drwaings()
    img = cv2.imread('combined_image.jpg', cv2.IMREAD_GRAYSCALE)

    # Aplicar detector de bordas Canny
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    cv2.imshow('Resultado', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()

#   This program - and EVERY file attached to it - is confidential and non-free software.
#   It has not been licensed yet and should not be redistributed. Created by joaopedro.torres@nov.com
#   at NOV Flexibles. It belongs to NOV Flexibles AND João Pedro de Sousa Torres Costa.

