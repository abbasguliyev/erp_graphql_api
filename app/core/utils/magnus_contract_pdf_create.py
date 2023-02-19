import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image
from contract.models import Installment

from core.settings import BASE_DIR, __PRODUCTION__
module_dir = os.path.dirname(__file__)  # get current directory


def magnus_contract_pdf_canvas(customer, contract) -> list:
    fullname = customer.fullname
    fullname_split = fullname.split(" ")

    if customer.phone_number_1 is not None:
        phone_number_1 = customer.phone_number_1
    else:
        phone_number_1 = ""
    if customer.phone_number_2 is not None:
        phone_number_2 = customer.phone_number_2
    else:
        phone_number_2 = ""

    if customer.address is not None:
        address = customer.address
    else:
        address = ""

    if customer.region is not None:
        region = customer.region.region_name
    else:
        region = ""

    day = contract.contract_date.day
    month = contract.contract_date.month
    year = contract.contract_date.year
    product_name = contract.product.product_name

    if __PRODUCTION__ == True:
        try:
            signature = os.path.join(
                BASE_DIR, f"{contract.electronic_signature}")
        except:
            signature = None
    else:
        signature = None

    new_pdfs = []

    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    i = 0
    while i < 3:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('DejaVuSans', 12)
        if i == 0:
            can.drawString(55, 654, f"{region}")
            can.drawString(413, 654, f"{day}")
            can.drawString(455, 654, f"{month} {year}")
            can.drawString(50, 543, f"{fullname}")
            can.drawString(280, 433, f"{product_name}")
            can.save()
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            new_pdfs.append(new_pdf)
        if i == 1:
            can.drawString(155, 696, f"{product_name}")
            can.drawString(330, 634, f"{product_name}")
            can.save()
            packet.seek(0)
            new_pdf1 = PdfFileReader(packet)
            new_pdfs.append(new_pdf1)
        if i == 2:
            can.drawString(352, 661, f"{product_name}")
            if len(fullname_split) == 1:
                can.drawString(405, 444, f"{fullname_split[0]}")
            elif len(fullname_split) == 2:
                can.drawString(
                    405, 444, f"{fullname_split[0]} {fullname_split[1]}")
            elif len(fullname_split) == 3:
                can.drawString(
                    405, 444, f"{fullname_split[0]} {fullname_split[1]}")
                can.drawString(340, 418, f"{fullname_split[2]}")
            elif len(fullname_split) == 4:
                can.drawString(
                    405, 444, f"{fullname_split[0]} {fullname_split[1]}")
                can.drawString(
                    340, 418, f"{fullname_split[2]} {fullname_split[3]}")

            can.drawString(373, 382, f"{phone_number_1} {phone_number_2}")
            can.drawString(413, 352, f"{address[:21]}")
            can.drawString(308, 327, f"{address[21:60]}")
            can.drawString(308, 300, f"{address[60:100]}")

            if signature is not None:
                can.drawImage(x=342, y=190, image=signature,
                              width=200, height=30)
            else:
                can.drawString(342, 190, f"Imza")

            can.save()
            packet.seek(0)
            new_pdf1 = PdfFileReader(packet)
            new_pdfs.append(new_pdf1)
        i += 1

    return new_pdfs


def magnus_create_contract_pdf(canvas, contract):
    new_pdfs = canvas
    # read your existing PDF
    file_path = os.path.join(
        BASE_DIR, 'media/media/contract_doc/magnus-contract.pdf')
    file_path_new = os.path.join(
        f'media/media/contract_doc/installment/magnus-contract-{contract.pk}.pdf')

    existing_pdf = PdfFileReader(
        open(file_path, "rb")
    )
    page_numbers = existing_pdf.pages.lengthFunction()
    output = PdfFileWriter()

    page1 = existing_pdf.getPage(0)
    page2 = existing_pdf.getPage(1)
    page3 = existing_pdf.getPage(2)
    page4 = existing_pdf.getPage(3)

    # 1-ci sehife
    page1.merge_page(new_pdfs[0].getPage(0))
    output.addPage(page1)

    outputStream1 = open(
        file_path_new,
        "wb")
    output.write(outputStream1)
    outputStream1.close()

    # 2-ci sehife
    output.addPage(page2)

    # 3-cu sehife
    page3.merge_page(new_pdfs[1].getPage(0))
    output.addPage(page3)
    # finally, write "output" to a real file
    outputStream2 = open(
        file_path_new,
        "wb")
    output.write(outputStream2)
    outputStream2.close()

    # 4-cu sehife
    page4.merge_page(new_pdfs[2].getPage(0))
    output.addPage(page4)

    # finally, write "output" to a real file
    outputStream3 = open(
        file_path_new,
        "wb")
    output.write(outputStream3)
    outputStream3.close()

    return file_path_new


def magnus_installment_contract_pdf_canvas(contract) -> list:
    day = contract.contract_date.day
    month = contract.contract_date.month
    year = contract.contract_date.year

    region = contract.customer.region.region_name
    customer = contract.customer

    payment_style = contract.payment_style

    fullname = contract.customer.fullname
    fullname_split = fullname.split(" ")
    if customer.phone_number_1 is not None:
        phone_number_1 = customer.phone_number_1
    else:
        phone_number_1 = ""
    if customer.phone_number_2 is not None:
        phone_number_2 = customer.phone_number_2
    else:
        phone_number_2 = ""

    if customer.address is not None:
        address = customer.address
    else:
        address = ""

    product_name = contract.product.product_name
    product_quantity = contract.product_quantity

    if __PRODUCTION__ == True:
        try:
            signature = os.path.join(
                BASE_DIR, f"{contract.electronic_signature}")
        except:
            signature = None
    else:
        signature = None

    product_price = contract.product.price
    initial_payment = contract.initial_payment
    if initial_payment == None or initial_payment == "":
        initial_payment = 0
    initial_payment_debt = contract.initial_payment_debt
    if initial_payment_debt == None or initial_payment_debt == "":
        initial_payment_debt = 0
    initial_payment_full = float(initial_payment) + float(initial_payment_debt)
    negd_odenis_2 = contract.negd_odenis_2
    if contract.initial_payment_status == "BİTMİŞ":
        remaining_debt = float(product_price) - float(initial_payment)
    else:
        remaining_debt = float(product_price) - float(initial_payment_full)

    installment_list = []
    installment = Installment.objects.filter(contract=contract)

    installment_list = list(installment)

    new_pdfs = []

    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

    i = 0
    while i < 4:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('DejaVuSans', 12)

        if i == 0:
            can.drawString(223, 695, f"{day}")
            can.drawString(253, 695, f"{month}   {year}")

            can.drawString(80, 633, f"{region}")

            can.drawString(395, 633, f"{day}")
            can.drawString(430, 633, f"{month}   {year}")

            can.drawString(65, 520, f"{fullname}")

            can.drawString(65, 440, f"{product_name}")

            can.drawString(85, 380, f"{product_price}")
            if payment_style == "KREDİT":
                can.drawString(200, 380, f"{initial_payment}")
                can.drawString(305, 380, f"{initial_payment_debt}")
                can.drawString(380, 380, f"{remaining_debt}")
            else:
                can.drawString(200, 380, "0")
                can.drawString(305, 380, "0")
                can.drawString(380, 380, "0")

            if payment_style == "KREDİT":
                can.drawString(470, 380, f"{payment_style}")
            else:
                can.drawString(470, 380, "NƏĞD")

            x1 = 95
            x2 = 126
            x3 = 150
            x4 = 220

            zx1 = 377
            zx2 = 408
            zx3 = 427
            zx4 = 492

            if payment_style == "KREDİT":
                try:
                    can.drawString(
                        x1, 328, f"{installment_list[0].date.day}")
                    can.drawString(
                        x2, 328, f"{installment_list[0].date.month}")
                    can.drawString(
                        x3, 328, f"{installment_list[0].date.year}")
                    can.drawString(
                        x4, 325, f"{installment_list[0].price}")
                except:
                    can.drawString(x1, 328, f"")
                    can.drawString(x2, 328, f"")
                    can.drawString(x3, 328, f"")
                    can.drawString(x4, 325, f"")

                try:
                    can.drawString(
                        x1, 304, f"{installment_list[1].date.day}")
                    can.drawString(
                        x2, 304, f"{installment_list[1].date.month}")
                    can.drawString(
                        x3, 304, f"{installment_list[1].date.year}")
                    can.drawString(
                        x4, 295, f"{installment_list[1].price}")
                except:
                    can.drawString(x1, 304, f"")
                    can.drawString(x2, 304, f"")
                    can.drawString(x3, 304, f"")
                    can.drawString(x4, 295, f"")
                try:
                    can.drawString(
                        x1, 281, f"{installment_list[2].date.day}")
                    can.drawString(
                        x2, 281, f"{installment_list[2].date.month}")
                    can.drawString(
                        x3, 281, f"{installment_list[2].date.year}")
                    can.drawString(
                        x4, 275, f"{installment_list[2].price}")
                except:
                    can.drawString(x1, 281, f"")
                    can.drawString(x2, 281, f"")
                    can.drawString(x3, 281, f"")
                    can.drawString(x4, 275, f"")
                try:
                    can.drawString(
                        x1, 257, f"{installment_list[3].date.day}")
                    can.drawString(
                        x2, 257, f"{installment_list[3].date.month}")
                    can.drawString(
                        x3, 257, f"{installment_list[3].date.year}")
                    can.drawString(
                        x4, 248, f"{installment_list[3].price}")
                except:
                    can.drawString(x1, 257, f"")
                    can.drawString(x2, 257, f"")
                    can.drawString(x3, 257, f"")
                    can.drawString(x4, 248, f"")
                try:
                    can.drawString(
                        x1, 233, f"{installment_list[4].date.day}")
                    can.drawString(
                        x2, 233, f"{installment_list[4].date.month}")
                    can.drawString(
                        x3, 233, f"{installment_list[4].date.year}")
                    can.drawString(
                        x4, 226, f"{installment_list[4].price}")
                except:
                    can.drawString(x1, 233, f"")
                    can.drawString(x2, 233, f"")
                    can.drawString(x3, 233, f"")
                    can.drawString(x4, 226, f"")
                try:
                    can.drawString(
                        x1, 209, f"{installment_list[5].date.day}")
                    can.drawString(
                        x2, 209, f"{installment_list[5].date.month}")
                    can.drawString(
                        x3, 209, f"{installment_list[5].date.year}")
                    can.drawString(
                        x4, 203, f"{installment_list[5].price}")
                except:
                    can.drawString(x1, 209, f"")
                    can.drawString(x2, 209, f"")
                    can.drawString(x3, 209, f"")
                    can.drawString(x4, 203, f"")
                try:
                    can.drawString(
                        x1, 185, f"{installment_list[6].date.day}")
                    can.drawString(
                        x2, 185, f"{installment_list[6].date.month}")
                    can.drawString(
                        x3, 185, f"{installment_list[6].date.year}")
                    can.drawString(
                        x4, 180, f"{installment_list[6].price}")
                except:
                    can.drawString(x1, 185, f"")
                    can.drawString(x2, 185, f"")
                    can.drawString(x3, 185, f"")
                    can.drawString(x4, 180, f"")
                try:
                    can.drawString(
                        x1, 160, f"{installment_list[7].date.day}")
                    can.drawString(
                        x2, 160, f"{installment_list[7].date.month}")
                    can.drawString(
                        x3, 160, f"{installment_list[7].date.year}")
                    can.drawString(
                        x4, 156, f"{installment_list[7].price}")
                except:
                    can.drawString(x1, 160, f"")
                    can.drawString(x2, 160, f"")
                    can.drawString(x3, 160, f"")
                    can.drawString(x4, 156, f"")
                try:
                    can.drawString(
                        x1, 137, f"{installment_list[8].date.day}")
                    can.drawString(
                        x2, 137, f"{installment_list[8].date.month}")
                    can.drawString(
                        x3, 137, f"{installment_list[8].date.year}")
                    can.drawString(
                        x4, 132, f"{installment_list[8].price}")
                except:
                    can.drawString(x1, 137, f"")
                    can.drawString(x2, 137, f"")
                    can.drawString(x3, 137, f"")
                    can.drawString(x4, 132, f"")
                try:
                    can.drawString(
                        x1, 112, f"{installment_list[9].date.day}")
                    can.drawString(
                        x2, 112, f"{installment_list[9].date.month}")
                    can.drawString(
                        x3, 112, f"{installment_list[9].date.year}")
                    can.drawString(
                        x4, 108, f"{installment_list[9].price}")
                except:
                    can.drawString(x1, 112, f"")
                    can.drawString(x2, 112, f"")
                    can.drawString(x3, 112, f"")
                    can.drawString(x4, 108, f"")
                try:
                    can.drawString(
                        x1, 89, f"{installment_list[10].date.day}")
                    can.drawString(
                        x2, 89, f"{installment_list[10].date.month}")
                    can.drawString(
                        x3, 89, f"{installment_list[10].date.year}")
                    can.drawString(
                        x4, 84, f"{installment_list[10].price}")
                except:
                    can.drawString(x1, 89, f"")
                    can.drawString(x2, 89, f"")
                    can.drawString(x3, 89, f"")
                    can.drawString(x4, 84, f"")
                try:
                    can.drawString(
                        x1, 65, f"{installment_list[11].date.day}")
                    can.drawString(
                        x2, 65, f"{installment_list[11].date.month}")
                    can.drawString(
                        x3, 65, f"{installment_list[11].date.year}")
                    can.drawString(
                        x4, 60, f"{installment_list[11].price}")
                except:
                    can.drawString(x1, 65, f"")
                    can.drawString(x2, 65, f"")
                    can.drawString(x3, 65, f"")
                    can.drawString(x4, 60, f"")

                # 13 - 24

                try:
                    can.drawString(
                        zx1, 328, f"{installment_list[12].date.day}")
                    can.drawString(
                        zx2, 328, f"{installment_list[12].date.month}")
                    can.drawString(
                        zx3, 328, f"{installment_list[12].date.year}")
                    can.drawString(
                        zx4, 325, f"{installment_list[12].price}")
                except:
                    can.drawString(zx1, 328, f"")
                    can.drawString(zx2, 328, f"")
                    can.drawString(zx3, 328, f"")
                    can.drawString(zx4, 325, f"")

                try:
                    can.drawString(
                        zx1, 304, f"{installment_list[13].date.day}")
                    can.drawString(
                        zx2, 304, f"{installment_list[13].date.month}")
                    can.drawString(
                        zx3, 304, f"{installment_list[13].date.year}")
                    can.drawString(
                        zx4, 295, f"{installment_list[13].price}")
                except:
                    can.drawString(zx1, 304, f"")
                    can.drawString(zx2, 304, f"")
                    can.drawString(zx3, 304, f"")
                    can.drawString(zx4, 295, f"")
                try:
                    can.drawString(
                        zx1, 281, f"{installment_list[14].date.day}")
                    can.drawString(
                        zx2, 281, f"{installment_list[14].date.month}")
                    can.drawString(
                        zx3, 281, f"{installment_list[14].date.year}")
                    can.drawString(
                        zx4, 275, f"{installment_list[14].price}")
                except:
                    can.drawString(zx1, 281, f"")
                    can.drawString(zx2, 281, f"")
                    can.drawString(zx3, 281, f"")
                    can.drawString(zx4, 275, f"")
                try:
                    can.drawString(
                        zx1, 257, f"{installment_list[15].date.day}")
                    can.drawString(
                        zx2, 257, f"{installment_list[15].date.month}")
                    can.drawString(
                        zx3, 257, f"{installment_list[15].date.year}")
                    can.drawString(
                        zx4, 248, f"{installment_list[15].price}")
                except:
                    can.drawString(zx1, 257, f"")
                    can.drawString(zx2, 257, f"")
                    can.drawString(zx3, 257, f"")
                    can.drawString(zx4, 248, f"")
                try:
                    can.drawString(
                        zx1, 233, f"{installment_list[16].date.day}")
                    can.drawString(
                        zx2, 233, f"{installment_list[16].date.month}")
                    can.drawString(
                        zx3, 233, f"{installment_list[16].date.year}")
                    can.drawString(
                        zx4, 226, f"{installment_list[16].price}")
                except:
                    can.drawString(zx1, 233, f"")
                    can.drawString(zx2, 233, f"")
                    can.drawString(zx3, 233, f"")
                    can.drawString(zx4, 226, f"")
                try:
                    can.drawString(
                        zx1, 209, f"{installment_list[17].date.day}")
                    can.drawString(
                        zx2, 209, f"{installment_list[17].date.month}")
                    can.drawString(
                        zx3, 209, f"{installment_list[17].date.year}")
                    can.drawString(
                        zx4, 203, f"{installment_list[17].price}")
                except:
                    can.drawString(zx1, 209, f"")
                    can.drawString(zx2, 209, f"")
                    can.drawString(zx3, 209, f"")
                    can.drawString(zx4, 203, f"")
                try:
                    can.drawString(
                        zx1, 185, f"{installment_list[18].date.day}")
                    can.drawString(
                        zx2, 185, f"{installment_list[18].date.month}")
                    can.drawString(
                        zx3, 185, f"{installment_list[18].date.year}")
                    can.drawString(
                        zx4, 180, f"{installment_list[18].price}")
                except:
                    can.drawString(zx1, 185, f"")
                    can.drawString(zx2, 185, f"")
                    can.drawString(zx3, 185, f"")
                    can.drawString(zx4, 180, f"")
                try:
                    can.drawString(
                        zx1, 160, f"{installment_list[19].date.day}")
                    can.drawString(
                        zx2, 160, f"{installment_list[19].date.month}")
                    can.drawString(
                        zx3, 160, f"{installment_list[19].date.year}")
                    can.drawString(
                        zx4, 156, f"{installment_list[19].price}")
                except:
                    can.drawString(zx1, 160, f"")
                    can.drawString(zx2, 160, f"")
                    can.drawString(zx3, 160, f"")
                    can.drawString(zx4, 156, f"")
                try:
                    can.drawString(
                        zx1, 137, f"{installment_list[20].date.day}")
                    can.drawString(
                        zx2, 137, f"{installment_list[20].date.month}")
                    can.drawString(
                        zx3, 137, f"{installment_list[20].date.year}")
                    can.drawString(
                        zx4, 132, f"{installment_list[20].price}")
                except:
                    can.drawString(zx1, 137, f"")
                    can.drawString(zx2, 137, f"")
                    can.drawString(zx3, 137, f"")
                    can.drawString(zx4, 132, f"")
                try:
                    can.drawString(
                        zx1, 112, f"{installment_list[21].date.day}")
                    can.drawString(
                        zx2, 112, f"{installment_list[21].date.month}")
                    can.drawString(
                        zx3, 112, f"{installment_list[21].date.year}")
                    can.drawString(
                        zx4, 108, f"{installment_list[21].price}")
                except:
                    can.drawString(zx1, 112, f"")
                    can.drawString(zx2, 112, f"")
                    can.drawString(zx3, 112, f"")
                    can.drawString(zx4, 108, f"")
                try:
                    can.drawString(
                        zx1, 89, f"{installment_list[22].date.day}")
                    can.drawString(
                        zx2, 89, f"{installment_list[22].date.month}")
                    can.drawString(
                        zx3, 89, f"{installment_list[22].date.year}")
                    can.drawString(
                        zx4, 84, f"{installment_list[22].price}")
                except:
                    can.drawString(zx1, 89, f"")
                    can.drawString(zx2, 89, f"")
                    can.drawString(zx3, 89, f"")
                    can.drawString(zx4, 84, f"")
                try:
                    can.drawString(
                        zx1, 65, f"{installment_list[23].date.day}")
                    can.drawString(
                        zx2, 65, f"{installment_list[23].date.month}")
                    can.drawString(
                        zx3, 65, f"{installment_list[23].date.year}")
                    can.drawString(
                        zx4, 60, f"{installment_list[23].price}")
                except:
                    can.drawString(zx1, 65, f"")
                    can.drawString(zx2, 65, f"")
                    can.drawString(zx3, 65, f"")
                    can.drawString(zx4, 60, f"")

            can.save()
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            new_pdfs.append(new_pdf)
        if i == 1:
            can.drawString(73, 776, f"{product_name}")
            can.drawString(328, 776, f"{product_quantity}")
            can.drawString(266, 554, f"{fullname}")
            if signature is not None:
                can.drawImage(x=400, y=555, image=signature,
                              width=200, height=30)
            else:
                can.drawString(400, 555, f"Imza")

            can.drawString(70, 462, f"{day}")
            can.drawString(110, 462, f"{month}     {year}")

            if len(fullname_split) == 1:
                can.drawString(420, 302, f"{fullname_split[0]}")
            elif len(fullname_split) == 2:
                can.drawString(
                    420, 302, f"{fullname_split[0]} {fullname_split[1]}")
            elif len(fullname_split) == 3:
                can.drawString(
                    420, 302, f"{fullname_split[0]} {fullname_split[1]}")
                can.drawString(340, 274, f"{fullname_split[2]}")
            elif len(fullname_split) == 4:
                can.drawString(
                    420, 302, f"{fullname_split[0]} {fullname_split[1]}")
                can.drawString(
                    340, 274, f"{fullname_split[2]} {fullname_split[3]}")

            can.drawString(361, 220, f"{address[:22]}")
            can.drawString(316, 193, f"{address[22:60]}")
            can.drawString(316, 166, f"{address[60:99]}")

            # can.drawString(361, 95, f"Imza")
            if signature is not None:
                can.drawImage(x=361, y=95, image=signature,
                              width=200, height=30)
            else:
                can.drawString(361, 95, f"Imza")
            can.save()
            packet.seek(0)
            new_pdf1 = PdfFileReader(packet)
            new_pdfs.append(new_pdf1)
        i += 1

    return new_pdfs


def magnus_installment_create_contract_pdf(canvas, contract):
    new_pdfs = canvas
    # read your existing PDF
    file_path = os.path.join(
        BASE_DIR, 'media/media/contract_doc/magnus-contract-credit.pdf')
    file_path_new = os.path.join(
        f'media/media/contract_doc/installment/magnus-contract-credit-{contract.pk}.pdf')

    existing_pdf = PdfFileReader(
        open(file_path, "rb")
    )
    page_numbers = existing_pdf.pages.lengthFunction()
    output = PdfFileWriter()

    page1 = existing_pdf.getPage(0)
    page2 = existing_pdf.getPage(1)

    # 1-ci sehife
    page1.merge_page(new_pdfs[0].getPage(0))
    output.addPage(page1)

    outputStream1 = open(
        file_path_new,
        "wb")
    output.write(outputStream1)
    outputStream1.close()

    # 3-cu sehife
    page2.merge_page(new_pdfs[1].getPage(0))
    output.addPage(page2)
    # finally, write "output" to a real file
    outputStream2 = open(
        file_path_new,
        "wb")
    output.write(outputStream2)
    outputStream2.close()

    return file_path_new
