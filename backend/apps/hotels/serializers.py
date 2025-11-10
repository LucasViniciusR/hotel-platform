import boto3
from rest_framework import serializers

from config import settings
from .models import Hotel, Room, RoomImage


class RoomImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = RoomImage
        fields = ['id', 'caption', 'uploaded_at', 'url']

    def get_url(self, obj):
        if not obj.image:
            return None

        s3_client = boto3.client('s3', 
                                 region_name=settings.AWS_S3_REGION_NAME, 
                                 config=boto3.session.Config(signature_version='s3v4'), 
                                 endpoint_url='https://s3.us-east-2.amazonaws.com',
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID)

        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': obj.image.name
            },
            ExpiresIn=3600
        )
        return url

class RoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['id', 'number', 'type', 'price', 'is_available', 'images']

class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'description', 'rooms']
