from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


def index(request):
    return render(request, 'uploader.html', {})
def submit(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        filelocation=r'D:\django\cropcalendar'+ str(uploaded_file_url).replace("/",'\\')
        upload_gs='gsutil -m cp '+filelocation+'  gs://shpgee/'
        upload_gee=r'earthengine upload table --asset_id=users/ashok_dahal/cropsites/'+str(filename).replace('.zip','')+' gs://shpgee/'+filename
        stream = os.popen(upload_gs)
        stream2 = os.popen(upload_gee)
        output = stream.read()
        
        return render(request, 'thankyou.html', {
            'uploaded_file_url': filelocation,'filename':filename
        })
    else:
        return render(request, 'uploader.html', {})

