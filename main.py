#  Copyright (C) 2023 João Pedro de S. T. Costa; read end of file for more information

from pdfUtils import *

def main():
    instance = Pdfutils(pdf_path)
    drawings = instance.get_possible_drwaings()
    final_image = instance.create_combined_image(drawings)
    final_image.save("combined_image.jpg")

main()

#   This program is a confidential and non-free software. It has not
#   been licensed yet. Created by joaopedro.torres@nov.com and belongs
#   to NOV Flexibles.

