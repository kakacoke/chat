import fitz
from django.http import HttpResponse
from django.shortcuts import render
from langchain.embeddings import OpenAIEmbeddings

from apps.embedding.models import PDFEmbedding


# Create your views here.类似services和dao

# 读取并分块处理pdf
def split_pdf_to_chunks(file_path, chunk_size=512):
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()

    text_splitter = PDFTextSplitter(chunk_size=chunk_size)
    chunks = text_splitter.split(text)
    return chunks


# 指定模型向量化处理文本块
def vectorize_chunks(chunks):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectors = [embeddings.embed(chunk) for chunk in chunks]
    return vectors


# 存储向量到数据库
def process_pdf_to_database(file_path):
    chunks = split_pdf_to_chunks(file_path)
    vectors = vectorize_chunks(chunks)

    for chunk, vector in zip(chunks, vectors):
        embedding = PDFEmbedding(chunk=chunk, vector=vector)
        embedding.save()


# 上传pdf
def upload_pdf(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        with open('temp.pdf', 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        process_pdf_to_database('temp.pdf')
        return HttpResponse("PDF processed and saved to database.")

    return render(request, 'upload.html')
