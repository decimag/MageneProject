import mimetypes

from django.http import HttpResponse

...

def download_file(request):
    # fill these variables with real values
    flPath="C:/Users/cmag2/PycharmProjects/MageneProject/MageneApp/static/ged/GEDCOM Lilou 27 Octobre 2020.GED"
    flName="GEDCOM Lilou 27 Octobre 2020.GED"
    fl = open(flPath, 'r')
    mime_type, _ = mimetypes.guess_type(flPath)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % flName
    return response