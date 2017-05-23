from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','first_name','last_name','email','password','phone','status','created_date')

class UserTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','first_name','last_name','email','phone','worker')


class WorkerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Worker
		fields = ('id','user','photo_url','description','experience','rating','status')

class WorkerTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Worker
		fields = ('id','photo_url','description','experience','rating')


class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ('id','user','tag','description','latitude','longitude')

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('id','user','worker','date','value','comment')

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id','description')

class SubcategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Subcategory
		fields = ('id','category','description')

class JobRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = JobRequest
		fields = ('id','user','subcategory','address','date_min','date_max','comment','status','pub_date')

class PhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Photo
		fields = ('id','jobRequest','photo_url')

class JobApplicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = JobApplication
		fields = ('id','worker','jobRequest','price','priceManos','comment','status')

class LoginSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email','password')

