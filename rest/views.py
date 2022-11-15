from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, mixins
# import ffmpeg_streaming
# from ffmpeg_streaming import Formats
from urllib.parse import urlparse
import os
import boto3
import time
from django.conf import settings
from rest_framework import status
import sys
import os

import moviepy.editor as moviepy


def aws_session(accessKey,secretKey,region):
    return boto3.session.Session(aws_access_key_id=str(accessKey),
                                aws_secret_access_key=str(secretKey),
                                region_name=str(region))


def upload_file_to_bucket(bucket_name, file_path,accessKey,secretKey,region):
    session = aws_session(accessKey,secretKey,region)
    s3_resource = session.resource('s3')
    file_name = os.path.basename(file_path)
    name, ext = os.path.splitext(file_name)
    aws_file_path  ="post_attachment/{}.mp4".format(name)
    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(
      Filename=file_path,
      Key=aws_file_path,
    )

    s3_video_name = name+".mp4"
    return s3_video_name

class UploadAwsFile(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        content = {'Success'}
        return Response(content, status=status.HTTP_200_OK)

    def post(self,request, *args, **kwargs):
        # try:

        res = {}
        resStatus = 200
        # video = ffmpeg_streaming.input('https://assets-simpleonline.s3.us-east-2.amazonaws.com/directory1/directory2/4c2b4d28cb442fc02fa46d87bc5b7e9e_waoo+666138.m3u8')
        data = request.data
        urlLink = str(data.get("fileName"))
        bucket_name = str(data.get("bucket"))
        accessKey = str(data.get("accessKey"))
        secretKey = str(data.get("secretKey"))
        region = str(data.get("region"))
        # video = ffmpeg_streaming.input(urlLink)
        # print(video)
        # stream = video.stream2file(Formats.h264())
        ts = time.time()
        name, ext = os.path.splitext(str(ts))
        new_name = "live_video_{}.{}".format(name,'mp4')
        full_path = os.path.join(settings.MEDIA_ROOT,new_name)
        # stream.output(full_path)
        clip = moviepy.VideoFileClip(urlLink)
        clip.write_videofile(full_path)
        s3_url = upload_file_to_bucket(bucket_name, full_path,accessKey,secretKey,region)

        res["live_video_name"] = s3_url
        full_path = os.path.join(settings.MEDIA_ROOT,new_name)
        os.remove(full_path)
        # except:
        #     resStatus=400
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print("line no is ",exc_type, exc_tb.tb_lineno)
        #     res = {"status":"failure"}
        return Response(res, status=resStatus)
        


class homeView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        content = {'Wellcome'}
        return Response(content, status=status.HTTP_200_OK)


