#  Copyright (C) 2023 João Pedro de S. T. Costa; read end of file for more information
import cv2
import pytesseract
from pytesseract import Output
from pdfUtils import *




def main():
    instance = Pdfutils(pdf_path)
    drawings = instance.get_possible_drwaings()
    img = cv2.imread('combined_image.jpg', cv2.IMREAD_GRAYSCALE)

    # Aplicando a transformada de Hough para encontrar linhas
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, minLineLength=1000, maxLineGap=10)

    # Desenhando as linhas encontradas
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Reconhecendo texto com pytesseract
    d = pytesseract.image_to_data(img, output_type=Output.DICT)

    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            if "(CONE LENGTH)" in d['text'][i]:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Recortando a imagem
                roi = img[y:y + h, x:x + w]
                cv2.imshow('Resultado', roi)

    cv2.imshow('Resultado', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()

#   This program is a confidential and non-free software. It has not
#   been licensed yet. Created by joaopedro.torres@nov.com and belongs
#   to NOV Flexibles.

