from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
import boto3
import re


def index(request):
    context = {}
    if request.method == "GET":
        return render(request,'polls/index.html',context)

    if request.method == "POST":
        image = request.FILES['file']
        filename = image.name
        client = boto3.client('s3')
        client.upload_fileobj(image, "memoirebuckettest", filename)
        return HttpResponse("image uploaded")

def getImage(request,filename):
    extension = re.split(r'\.',filename)[1]
    print extension
    client = boto3.client('s3')
    client.download_file("memoirebuckettest",filename,"/tmp/{}".format(filename))
    with open("/tmp/{}".format(filename), "rb") as f:
        return HttpResponse(f.read(),content_type="image/{}".format(extension))

