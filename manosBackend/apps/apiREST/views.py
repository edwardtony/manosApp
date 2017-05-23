from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from apps.apiREST.models import *
from apps.apiREST.serializers import *
from django.views.decorators.csrf import csrf_exempt

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from passlib.hash import pbkdf2_sha256

#-------------------------------GLOBAL VARIABLES-------------------------------

root = 'localhost:8000/'

# Create your views here.
#-------------------------------UTILS-------------------------------

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content,**kwargs)


def responseSuccess(data, links={}):
    result = {
        'data': data,
        '_links': [links],
    }
    return result

def responseError(userMessage = "", internalMessage = "", code = 0):
    result = {
        'errors': [
            {
                "userMessage" : userMessage,
                "internalMessage" : internalMessage,
                "code": code,
                "more info": "http://manosAPI/api/v1/errors/{code}".format(code=code)
            }
        ]
    }
    return result

def consoleLog(text='Información',data= ''):
    print('########## {text} : {data} ##########'.format(text=text, data=data))
#-------------------------------USER-------------------------------

@csrf_exempt
def user_list(request):
    """
    List all code user, or create a new user.
    """
    consoleLog('Endpoint consultado',request.build_absolute_uri(request.path))
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JSONResponse(serializer.data, status = 200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        enc_password = pbkdf2_sha256.encrypt(data['password'],rounds=12000,salt_size=32)
        data['password'] = enc_password
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            email = data.get('email')
            try:
                validate_email(email)
            except ValidationError as e:
                return JSONResponse(responseError('Introduzca una dirección de correo electrónico válida.','',), status=400)
            
            try:
                userTemp  = User.objects.get(email=email)
            except User.DoesNotExist as e:
                serializer.save()
                return JSONResponse(serializer.data, status=201)    

            return JSONResponse(responseError('Correo electrónico en uso.','',), status=400)
        return JSONResponse(serializer.errors, status=400)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve, update or delete a user.
    """
    consoleLog('Endpoint consultado',request.build_absolute_uri(request.path))

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)

        consoleLog('Cuerpo del uptade PUT',data)

        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)
    elif request.method == 'PATCH':
        data = JSONParser().parse(request)

        consoleLog('Cuerpo del update PATCH',data)

        for key,value in data.items():
            user.__dict__[key] = value
        user.save()
        return HttpResponse(status=200)
    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)
    else:
        return JSONResponse(responseError('Método {} no soportado para este recurso'.format(request.method),'',), status=400)


@csrf_exempt
def login(request):

    if request.method == 'POST':
        credentials = JSONParser().parse(request)
        consoleLog('Credenciales del Login',credentials)
        serializer = LoginSerializer(data = credentials)
        if serializer.is_valid():
            try:
                user = User.login(credentials.get("email"),credentials.get("password"))                
            except User.DoesNotExist as e:
                return JSONResponse(responseError('Correo o contraseña erronea','',),status=404)
            userSerializer = UserTransactionSerializer(user)
            data = {
                'user': userSerializer.data
            }
            try:
                worker = Worker.objects.get(user=user.id)
                data['user']['worker'] =  WorkerTransactionSerializer(worker).data
            except Worker.DoesNotExist as e:
                data['user']['worker'] =  {}

            links = {
                'self':{
                    'href':request.build_absolute_uri(request.path)
                },
                'requests':{
                    'href': root + 'users/{id_user}/job_requests/'.format(id_user=user.id)
                }
            }
            return JSONResponse(responseSuccess(data,links))
        else:
            return JSONResponse(serializer.errors, status=400)
        print(credentials)
    else:
        return  HttpResponse(status=404)


#-------------------------------ADDRESS-------------------------------

@csrf_exempt
def address_list(request):
    """
    List all code address request, or create a new address request.
    """

    if request.method == 'GET':
        address = Address.objects.all()
        serializer = AddressSerializer(address, many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def address_detail(request, pk):
    """
    Retrieve, update or delete a address request.
    """
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AddressSerializer(address)
        links = {
                'self':{
                    'href':request.build_absolute_uri(request.path)
                }
            }
        return JSONResponse(responseSuccess(serializer.data,links))

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AddressSerializer(address, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        address.delete()
        return HttpResponse(status=204)

@csrf_exempt
def addresses_list_by_user(request,pk):

    if request.method == 'GET':
        address = Address.objects.filter(user=pk)
        serializer = AddressSerializer(address, many=True)

        links = {
                'self':{
                    'href':request.build_absolute_uri(request.path)
                }
            }
        return JSONResponse(responseSuccess(serializer.data,links),status=200)
    else:
        return HttpResponse(status=404)



#-------------------------------JOBREQUEST-------------------------------

@csrf_exempt
def job_request_list(request):
    """
    List all code job request, or create a new job request.
    """

    if request.method == 'GET':
        d1 = request.GET.get('d1','')
        d2 = request.GET.get('d2','')
        d3 = request.GET.get('d3','')
        d4 = request.GET.get('d4','')
        d5 = request.GET.get('d5','')
        d6 = request.GET.get('d6','')
        d7 = request.GET.get('d7','')
        schedule = [d1,d2,d3,d4,d5,d6,d7]
        print(schedule)

        categories = request.GET.get('categories','')
        if categories != '':
            id_categories = [int(x) for x in categories.split(',')]
            print(id_categories)
            job_request = JobRequest.objects.filter(subcategory__in = id_categories)
        else:
            job_request = JobRequest.objects.all()
        serializer = JobRequestSerializer(job_request, many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print("hola")
        print(data)
        serializer = JobRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def job_request_detail(request, pk):
    """
    Retrieve, update or delete a job request.
    """
    try:
        job_request = JobRequest.objects.get(pk=pk)
    except JobRequest.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = JobRequestSerializer(job_request)
        links = {
                'self':{
                    'href':request.build_absolute_uri(request.path)
                },
                'applications':{
                    'href': root + 'job_request/{id_job_request}/job_applications/'.format(id_job_request=pk)
                }
            }
        return JSONResponse(responseSuccess(serializer.data,links))

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = JobRequestSerializer(job_request, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        job_request.delete()
        return HttpResponse(status=204)

@csrf_exempt
def job_requests_list_by_user(request, pk):

    if request.method == 'GET':
        job_request = JobRequest.objects.filter(user=pk)
        serializer = JobRequestSerializer(job_request, many=True)

        links = {
                'self':{
                    'href':request.build_absolute_uri(request.path)
                }
            }
        return JSONResponse(responseSuccess(serializer.data,links),status=200)
    else:
        return HttpResponse(status=404)

@csrf_exempt
def job_applications_list_by_request(request,pk):

    if request.method == 'GET':
        job_application = JobApplication.objects.filter(jobrequest = pk)
        serializer = JobApplicationSerializer(job_application, many=True)



    else:
        return JSONResponse(responseError('Método {} no soportado para este recurso'.format(request.method),'',), status=400)

@csrf_exempt
def job_request_cancel(request, pk):
    
    if request.method == 'GET':
        job_request = JobRequest.objects.get(pk=pk)
        job_request.status = "Anulado"
        job_request.save()
        print(job_request)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


#-------------------------------JOBAPPLICATION-------------------------------
@csrf_exempt
def job_application_list(request):
    """
    List all code job application, or create a new job application.
    """

    if request.method == 'GET':
        job_application = JobApplication.objects.all()
        serializer = JobRequestSerializer(job_application, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print("hola")
        print(data)
        serializer = JobApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def job_application_detail(request, pk):
    """
    Retrieve, update or delete a job application.
    """
    try:
        job_application = JobApplication.objects.get(pk=pk)
    except JobApplication.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = JobApplicationSerializer(user)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = JobApplicationSerializer(job_application, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        job_application.delete()
        return HttpResponse(status=204)

@csrf_exempt
def job_choose(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        pk_job_request = data.get("job_request")
        pk_job_applicant = data.get("job_application")

        job_request = JobRequest.objects.get(pk=pk_job_request)
        
        job_applicant = job_request.jobapplication_set.get(pk=pk_job_applicant)
        job_applicant.status = 'S'
        job_applicant.save()
        print(job_application)

        return HttpResponse(status=200)
    return HttpResponse(status=404)

@csrf_exempt
def job_not_choose(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        pk_job_request = data.get("job_request")
        pk_job_applicant = data.get("job_application")

        job_request = JobRequest.objects.get(pk=pk_job_request)
        
        job_applicant = job_request.jobapplication_set.get(pk=pk_job_applicant)
        job_applicant.status = 'N'
        job_applicant.save()
        print(job_application)

        return HttpResponse(status=200)
    return HttpResponse(status=404) 


#-------------------------------Comment-------------------------------
@csrf_exempt
def comment_list(request):
    """
    List all code comment, or create a new comment.
    """

    if request.method == 'GET':
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print("hola")
        print(data)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def comment_detail(request, pk):
    """
    Retrieve, update or delete a job application.
    """
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CommentSerializer(user)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        comment.delete()
        return HttpResponse(status=204)

@csrf_exempt
def comment_list_by_worker(request, pk):
    
    if request.method == 'GET':
        worker = Worker.objects.get(pk=pk)
        print(worker.comment_set.all())
        serializer = CommentSerializer(worker.comment_set.all(), many=True)
        return JSONResponse(serializer.data,status=200)
    else:
        return HttpResponse(status=404)


from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

class WorkerViewSet(viewsets.ModelViewSet):

    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

class AddressViewSet(viewsets.ModelViewSet):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):

    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class JobRequestViewSet(viewsets.ModelViewSet):

    queryset = JobRequest.objects.all()
    serializer_class = JobRequestSerializer

class PhotoViewSet(viewsets.ModelViewSet):

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):

    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
