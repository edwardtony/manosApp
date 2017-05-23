from django.db import models
from django.utils import timezone

from passlib.hash import pbkdf2_sha256

# Create your models here.

class User(models.Model):

	STATUS_CHOICES = (
		('ACTIVE','A'),
		('INACTIVE','I'),
	)

	first_name = models.CharField(max_length=30) #Obligatorio , No Blanco
	last_name = models.CharField(max_length=30, null = True, blank=True) 
	email = models.CharField(max_length=30) #Obligatorio , No Blanco
	password= models.CharField(max_length=150) #Obligatorio , No Blanco
	phone = models.IntegerField() #Obligatorio , No Blanco
	status = models.CharField(max_length=10, choices= STATUS_CHOICES, default="A") #Obligatorio , No Blanco
	created_date = models.DateTimeField(default=timezone.now()) #Obligatorio , No Blanco

	def verify_password(self, password):
		print(self.password)
		return pbkdf2_sha256.verify(password,self.password)

	def login(email,password):
		userTemp = User.objects.get(email=email)
		result = userTemp.verify_password(password)
		if result:
			return userTemp
		else:
			raise User.DoesNotExist
			return 0

	def __str__(self):
		return "{nombre} {apellido}".format(nombre = self.first_name, apellido = self.last_name)

class Worker(models.Model):
		
	STATUS_CHOICES = (
		('VALIDATED','V'),
		('UNVALIDATED','U'),
	)	

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	photo_url = models.CharField(max_length=200, null=True, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)
	experience = models.CharField(max_length=200, null=True, blank=True)
	rating = models.IntegerField(default=0) #Obligatorio , No Blanco
	status = models.CharField(max_length=10, choices= STATUS_CHOICES, default="U") #Obligatorio , No Blanco

	def __str__(self):
		return "{user} {rating}".format(user = self.user, rating = self.rating)

class Address(models.Model):
	user = models.ForeignKey(User, on_delete= models.CASCADE)
	tag = models.CharField(max_length=100) #Obligatorio , No Blanco
	description = models.CharField(max_length=500) #Obligatorio , No Blanco
	latitude = models.CharField(max_length=20) #Obligatorio , No Blanco
	longitude = models.CharField(max_length=20) #Obligatorio , No Blanco 

	def __str__(self):
		return "{user} {description} {longitude} {latitude}".format(user = self.user, description = self.description, longitude = self.longitude, latitude = self.latitude)

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	worker = models.ForeignKey(Worker, on_delete = models.CASCADE)
	date = models.DateTimeField(default=timezone.now()) #Obligatorio , No Blanco
	value = models.IntegerField(default=1) #Obligatorio , No Blanco
	comment = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return "{user} -> {worker} = {comment}".format(user= self.user , worker= self.worker ,comment = self.comment)

class Category(models.Model):
	description = models.CharField(max_length=40) 

	def __str__(self):
		return "{description}".format(description = self.description)

class Subcategory(models.Model):
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	description = models.CharField(max_length=40)

	def __str__(self):
		return "{category} {description}".format(category = self.category, description = self.description)

class JobRequest(models.Model):

	STATUS_CHOICES = (
		('CREATED','C'),
		('QUOTED','Q'),
		('FINISHED','F'),
	)	

	user = models.ForeignKey(User, on_delete = models.CASCADE)
	subcategory = models.ForeignKey(Subcategory, on_delete = models.CASCADE)
	address = models.ForeignKey(Address, on_delete = models.CASCADE)
	date_min = models.DateTimeField() #Obligatorio , No Blanco
	date_max = models.DateTimeField() #Obligatorio , No Blanco
	comment = models.CharField(max_length=100) #Obligatorio , No Blanco
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='C')
	pub_date = models.DateTimeField(default=timezone.now())

	def __str__(self):
		return "{user} {subcategory} {status}".format(user = self.user, subcategory = self.subcategory, status= self.status)

class Photo(models.Model):
	jobRequest = models.ForeignKey(JobRequest, on_delete=models.CASCADE)
	photo_url = models.CharField(max_length=200) #Obligatorio , No Blanco

	def __str__(self):
		return "{photo_url}".format(photo_url = self.photo_url)

class JobApplication(models.Model):

	STATUS_CHOICES = (
		('CHOSEN','C'),
		('WAITING','W'),
	)	

	worker = models.ForeignKey(Worker, on_delete = models.CASCADE) #Obligatorio , No Blanco
	jobRequest = models.ForeignKey(JobRequest, on_delete=models.CASCADE) #Obligatorio , No Blanco 
	price = models.DecimalField(max_digits=6 , decimal_places=2) #Obligatorio , No Blanco
	priceManos = models.DecimalField(max_digits=6 , decimal_places=2) #Obligatorio , No Blanco
	comment = models.CharField(max_length=100, null=True, blank=True) #Obligatorio , No Blanco
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='W') #Obligatorio , No Blanco

	def __str__(self):
		return "{worker} {jobRequest} {price} {status}".format(worker = self.worker, jobRequest = self.jobRequest, price= self.price, status= self.status)
