import datetime
import os
import time
import tkinter as tk
from io import BytesIO
from tkinter import filedialog

from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def select_pdf():
    pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    pdf_path.set(pdf_file)


def select_output_dir():
    output_dir = filedialog.askdirectory()
    output_path.set(output_dir)


def add_page_number(page_number, packet):
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 18)
    can.drawString(300, 20, str(page_number))
    can.save()


def add_page_numbers_from_range(input_file, output_file, start_page, end_page, start_number, end_number):
    """
    Add a custom range of page numbers to a PDF page range

    :param input_file: inputting pdf
    :param output_file: a new pdf
    :param start_page: the start page of the pdf
    :param end_page: the end page of the pdf
    :param start_number: the start number of the pagination
    :param end_number: the end number of the pagination
    :return: a new pdf with added page numbers
    """
    output = PdfWriter()
    input_pdf = PdfReader(input_file)
    total_pages = len(input_pdf.pages)
    if start_page < 1 or end_page > total_pages:
        print("valid page range")
        return

    if end_page - start_page != end_number - start_number:
        print("The range of pages should be same with the range of pagination")
        return

    page_number = start_number
    for i, page in enumerate(input_pdf.pages):
        if start_page <= i + 1 <= end_page:
            packet = BytesIO()
            add_page_number(page_number, packet)
            packet.seek(0)
            new_pdf = PdfReader(packet)
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)
            page_number += 1
        else:
            output.add_page(page)

    output_stream = open(output_file, "wb")
    output.write(output_stream)
    output_stream.close()


def add_page_numbers_func():
    start_time = time.time()
    input_pdf = pdf_path.get()
    output_dir = output_path.get() + "/"
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = os.path.join(output_dir, f"newpdf_{current_time}.pdf")
    # page
    start_num = start_page_pdf.get()
    end_num = end_page_pdf.get()
    # pagination
    start_page_num = start_page.get()
    end_page_num = end_page.get()
    add_page_numbers_from_range(input_pdf, output_dir, start_num, end_num, start_page_num, end_page_num)
    end_time = time.time()
    elapsed_time = end_time - start_time
    time_label.configure(text=f"cost time：{elapsed_time:.2f}seconds")


root = tk.Tk()
root.geometry("650x320")
root.title("AddPDFPagination")
root.configure(bg="#f7f7f7")

# the elements of the first row
row1 = tk.Frame(root, bg="#f7f7f7")
row1.pack(pady=10)

pdf_label = tk.Label(row1, text=" input PDF:", bg="#f7f7f7")
pdf_label.pack(side=tk.LEFT, padx=10)

pdf_path = tk.StringVar()
pdf_entry = tk.Entry(row1, textvariable=pdf_path, width=50)
pdf_entry.pack(side=tk.LEFT, padx=10)

pdf_button = tk.Button(row1, text="select file", command=select_pdf)
pdf_button.pack(side=tk.LEFT, padx=10)

# the elements of the second row
row2 = tk.Frame(root, bg="#f7f7f7")
row2.pack(pady=10)

output_label = tk.Label(row2, text="output dir:", bg="#f7f7f7")
output_label.pack(side=tk.LEFT, padx=10)

output_path = tk.StringVar()
output_entry = tk.Entry(row2, textvariable=output_path, width=50)
output_entry.pack(side=tk.LEFT, padx=10)

output_button = tk.Button(row2, text="select dir", command=select_output_dir)
output_button.pack(side=tk.LEFT, padx=10)

# the elements of the third row
row3 = tk.Frame(root, bg="#f7f7f7")
row3.pack(pady=10)

num_label = tk.Label(row3, text="custom pages:", bg="#f7f7f7")
num_label.pack(side=tk.LEFT, padx=10)

start_page_pdf = tk.IntVar()
start_entry_pdf = tk.Entry(row3, textvariable=start_page_pdf, width=10)
start_entry_pdf.pack(side=tk.LEFT, padx=5)

end_page_pdf = tk.IntVar()
end_entry_pdf = tk.Entry(row3, textvariable=end_page_pdf, width=10)
end_entry_pdf.pack(side=tk.LEFT, padx=5)

# the elements of the fourth row
row4 = tk.Frame(root, bg="#f7f7f7")
row4.pack(pady=10)

custom_label = tk.Label(row4, text="custom pagination:", bg="#f7f7f7")
custom_label.pack(side=tk.LEFT, padx=10)

start_page = tk.IntVar()
start_entry = tk.Entry(row4, textvariable=start_page, width=10)
start_entry.pack(side=tk.LEFT, padx=5)

end_page = tk.IntVar()
end_entry = tk.Entry(row4, textvariable=end_page, width=10)
end_entry.pack(side=tk.LEFT, padx=5)

# the elements of the fifth row
row5 = tk.Frame(root, bg="#f7f7f7")
row5.pack(pady=10)

add_button = tk.Button(row5, text="Add Pagination", command=add_page_numbers_func)
add_button.pack(side=tk.LEFT, padx=10)

# A label that shows the cost time
time_label = tk.Label(root, text="", bg="#f7f7f7")
time_label.pack(pady=10)

root.mainloop()
