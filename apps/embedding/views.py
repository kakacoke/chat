from django.shortcuts import render, redirect

from apps.embedding.models import PDFUploadForm


# Create your views here.类似services和dao
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_pdf')
    else:
        form = PDFUploadForm()
    return render(request, 'upload.html', {'form': form})
