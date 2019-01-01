from fpdf import FPDF
from pdf2image import convert_from_path
import math


def create_pv_image(pv, location_files):
    first_part = [
        ['Bureau de vote', pv.bv.name],
        ['Nombre d\'inscrits', str(pv.bv.register_num)],
        ['Nombre de votants', str(pv.bv.voters_num)]
    ]

    second_part = [
        ['Candidat', 'Nombre de voix']
    ]

    for r in pv.result:
        temp = []
        temp.append(r)
        temp.append(str(pv.result[r]))
        second_part.append(temp)

    pdf = FPDF()
    pdf.set_font("Times", style='B', size=20)
    pdf.add_page()
    row_height = pdf.font_size + 10
    i = 0
    for row in first_part:
        for item in row:
            if math.floor(i / 2) == i / 2:
                pdf.cell(62, row_height, txt=item, border=1)
            else:
                pdf.cell(130, row_height, txt=item, border=1)
            i = i + 1
        pdf.ln(row_height)
    pdf.ln(row_height)
    pdf.ln(row_height)
    i = 0
    for row in second_part:
        for item in row:
            if math.floor(i / 2) == i / 2:
                pdf.cell(140, row_height, txt=item, border=1)
            else:
                pdf.cell(52, row_height, txt=item, border=1)
            i = i + 1
        pdf.ln(row_height)
    pdf.output('{}/temp.pdf'.format(location_files))

    pages = convert_from_path('{}/temp.pdf'.format(location_files), dpi=200)
    for page in pages:
        page.save('{}/Images/{}/{}.JPEG'.format(location_files, pv.owner.replace(' ', '_'), pv.bv.name.replace(' ', '_')), 'JPEG')
