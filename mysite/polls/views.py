from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
import boto3


def index(request):
    context = {}
    if request.method == "GET":
        return render(request,'polls/index.html',context)

    if request.method == "POST":
        image = request.FILES['file']
        filename = image.name
        client = boto3.client('s3')
        ret = client.create_bucket(Bucket='memoirebuckettest')
        client.upload_fileobj(image, "memoirebuckettest", filename)
        return HttpResponse("image uploaded")
