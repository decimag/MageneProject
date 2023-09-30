import mimetypes

from django.http import HttpResponse
import os

...

def download_file(request):
    # fill these variables with real values
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    flPath=PROJECT_ROOT + "/static/ged/local102012_19-09-2023.ged"
    flName="GEDCOM Lilou 27 Octobre 2020.GED"
    fl = open(flPath, 'r')
    mime_type, _ = mimetypes.guess_type(flPath)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % flName
    return response