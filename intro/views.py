from django.shortcuts import render

def index(request):
    return render(request, 'intro.html', {})
#upload file
#gsutil -m cp districts.zip gs://shp/
#earthengine upload table --asset_id=users/ashok_dahal/cropsites/test gs://shp/districts.zip