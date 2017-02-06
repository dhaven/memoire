from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import boto3
import re

@login_required
def index(request):
    context = {}
    if request.method == "GET":
        data = {'username':request.user.username}
        return JsonResponse(data)

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

@login_required
def list(request,username):
    list_of_groups = []
    list_of_images = {}
    if request.user.username == username:
        for group in request.user.groups.all():
            list_of_groups.append(group.name + "/")
        client = boto3.client('s3')
        list_of_groups.append(username + "/")
        for prefix in list_of_groups:
            tempList = []
            response = client.list_objects(Bucket="memoirebuckettest",Prefix=prefix)
            for content in response['Contents']:
                imageName = re.sub(prefix,"",content['Key'])
                if imageName != "":
                    tempList.append(imageName)
            list_of_images[prefix] = tempList
    return JsonResponse(list_of_images)


