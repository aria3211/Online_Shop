from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .models import Product,Category
from accounts.models import User
from django.conf import settings as s
from .forms import PhotoForm
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from utils import test_func
from orders.forms import CartFrom
import boto3
import datetime
import os





LIARA = {
    'endpoint': s.LIARA_ENDPOINT,
    'accesskey': s.LIARA_ACCESS_KEY,
    'secretkey': s.LIARA_SECRET_KEY,
    'bucket': s.LIARA_BUCKET_NAME
}


class HomeView(View):
    def get(self,request,category_slug=None):
        products = Product.objects.filter(available=True) 
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            categoriy = Category.objects.get(slug=category_slug)
            products = products.filter(category=categoriy)
        return render(request,'home/home.html',{'products':products,'categories':categories})
    def post(self,request):
        pass

class DetailView(View):
    def get(self,request,slug):
        products = get_object_or_404(Product,slug=slug)
        form = CartFrom
        return render(request,'home/detail.html',{'product':products,'form':form})
      

      
@user_passes_test(test_func)
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo_instance = form.save(commit=False)

            default_category = Category.objects.get(id=2)
            # Get the original filename and extension
            
            photo_instance.category = default_category
            original_filename, file_extension = os.path.splitext(photo_instance.image.name)
            
            # Get current date and time
            current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Construct unique filename with date and original filename
            filename = f"{current_date}_{original_filename}{file_extension}"
            
            # Set the filename
            photo_instance.image.name = filename
            photo_instance.save()
            return redirect('home:bucket')
    else:
        form = PhotoForm()

    # Retrieve a list of uploaded photos from the S3 bucket
    s3 = boto3.client('s3',
        endpoint_url=LIARA['endpoint'],
        aws_access_key_id=LIARA['accesskey'],
        aws_secret_access_key=LIARA['secretkey']
    )
    bucket_name = LIARA['bucket']
    objects = s3.list_objects(Bucket=bucket_name)

    uploaded_photos = []
    if 'Contents' in objects:
        for obj in objects['Contents']:
            uploaded_photos.append({
                'name': obj['Key'],  # Assuming key name as file name
                'permanent_link': f"{LIARA['endpoint']}/{bucket_name}/{obj['Key']}",
                'temporary_link': s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket_name, 'Key': obj['Key']},
                    ExpiresIn=3600  # 1 hour expiry
                )
            })
    else:
        uploaded_photos.append({'name': 'no file', 'permanent_link': '', 'temporary_link': ''})

    return render(request, 'home/upload.html', {'form': form, 'uploaded_photos': uploaded_photos})


@user_passes_test(test_func)
def download_photo(request, photo_name):
    s3 = boto3.client('s3',
        endpoint_url=LIARA['endpoint'],
        aws_access_key_id=LIARA['accesskey'],
        aws_secret_access_key=LIARA['secretkey']
    )
    bucket_name = LIARA['bucket']
    file_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': photo_name},
        ExpiresIn=3600  # 1 hour expiry
    )
    return redirect(file_url)


@user_passes_test(test_func)
def delete_photo(request, photo_name):
    s3 = boto3.client('s3',
        endpoint_url=LIARA['endpoint'],
        aws_access_key_id=LIARA['accesskey'],
        aws_secret_access_key=LIARA['secretkey']
    )
    bucket_name = LIARA['bucket']
    s3.delete_object(Bucket=bucket_name, Key=photo_name)
    return redirect('upload_photo')