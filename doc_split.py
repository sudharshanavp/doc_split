import pikepdf  # pip install pikepdf
import os
from io import BytesIO

def split_pdf_into_n_page_chunks(input_pdf_path, output_folder,n=30):
    pdf = pikepdf.open(input_pdf_path)
    num_pages = len(pdf.pages)
    chunk_size = n  
    chunk_number = 1
    pdf_chunks = []  

    os.makedirs(output_folder, exist_ok=True)

    for start_page in range(0, num_pages, chunk_size):
        end_page = min(start_page + chunk_size, num_pages)

        new_pdf = pikepdf.Pdf.new()
        for page in range(start_page, end_page):
            new_pdf.pages.append(pdf.pages[page])

        #save to disk
        output_path = f"{output_folder}/chunk_{chunk_number}.pdf"
        new_pdf.save(output_path)
        print(f"Saved: {output_path}")

        #save as bytes
        pdf_bytes = BytesIO()
        new_pdf.save(pdf_bytes)
        pdf_bytes.seek(0)
        pdf_chunks.append(pdf_bytes)

        chunk_number += 1

    print(f"PDF split into {chunk_number - 1} chunks of up to 30 pages each!")
    return pdf_chunks

chunks = split_pdf_into_n_page_chunks("/content/pca merged.pdf", "/content",n=30)

# Example of accessing the byte content of a chunk
print(f"Number of chunks: {len(chunks)}")
first_chunk_bytes = chunks[0].getvalue()
