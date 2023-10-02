from django.shortcuts import redirect, render
from django.http import HttpResponse
from . models import *
from django.conf import settings
import os
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
from django.contrib import messages

# Load the pre-trained model
model_path = os.path.join(settings.BASE_DIR, 'home', 'models', 'skin_cancer_model.h5')
model = load_model(model_path)


# Create your views here.
def index(request):
    return render(request,'index.html')

def user_login(request):
      if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = patient_details.objects.filter(username=uname, password=passwd)
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].username
            
            return redirect("/user_home")
        else:
            messages.info(request,"Invalid credentials")
            context={'msg':'Login Error'}
            return redirect("/user_login")
      else:
          return render(request,'user_login.html')

def user_home(request):
    
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return user_login(request)

    context = {'uname':request.session['user_name']}
    return render(request,'user_home.html',context)


def user_register(request):
     



     if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        loc=request.POST["location"]
        location=Location.objects.get(id=loc)
        gender = request.POST.get('gender')
       
        addr = request.POST.get('addr')
        
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        uname = email
        if patient_details.objects.filter(email=email).exists():
            messages.info(request,"Username Already Exist! Please use different Email")
            return redirect("/user_register")
        else:
            new=patient_details.objects.create(fname=fname,lname=lname,gender=gender,addr=addr,location=location,email=email,contact=contact,username=uname,password=password)
            new.save()
            return redirect("/user_login")
     else:
         loc=Location.objects.all()
         context={'location':loc}
         return render(request,'user_details_add.html',context)
     
def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login(request)
    else:
        return user_login(request)
    


def new_test(request):
     
      if request.method == 'POST' and request.FILES['document']:
        uid = request.session['user_id']
        user=patient_details.objects.get(id=uid)
        # Get the uploaded image from the form
        uploaded_image = request.FILES['document']

        # Create a temporary file to store the uploaded image
        with open(os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg'), 'wb+') as temp_image:
            for chunk in uploaded_image.chunks():
                temp_image.write(chunk)

        # Load and preprocess the uploaded image
        img_width, img_height = 150, 150
        img = image.load_img(os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg'), target_size=(img_width, img_height))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        preprocessed_img = img_array / 255.0  # Normalize the image

        # Make prediction
        predictions = model.predict(preprocessed_img)
        print(f"predictions={predictions}")

        predicted_class = predictions[0][0]
        print(f"predicted class={predicted_class}")
        # Determine the result based on the prediction
        # if predicted_class < 0.5:
        #     result = "Benign"
        #     status="You have No Problem.You are Healthy.No need of any Doctor Consulting"

        # else:
        #     result = "Malignant"
        #     status="Please Immediately Visit a Nearby Doctor"
        if predicted_class > 0.79:
            result = "Not a skin image"
            status = "This image does not appear to be related to skin cancer."
        elif predicted_class < 0.5:
            result = "Benign"
            status = "You have No Problem. You are Healthy. No need for any Doctor Consulting."
        else:
            result = "Malignant"
            status = "Please Immediately Visit a Nearby Doctor"

        doctors=doctor_master.objects.filter(location=user.location)

        # Clean up: Delete the temporary image file
        os.remove(os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg'))
        print(result)
     
        new_report=patient_report.objects.create(patient=user,image=uploaded_image,result=result,status=status)
        new_report.save()
        return render(request, 'test_result.html', {'report': new_report,'result':result,'doctors':doctors})
      else:
          return render(request,'new_test.html')

def test_history(request):
    uid = request.session['user_id']
    user=patient_details.objects.get(id=uid)
    reports=patient_report.objects.filter(patient=user)

    context={'test_list':reports}
    return render(request,'patient_history.html',context)

#for pdf download options

from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from reportlab.platypus import Image

def generate_pdf_report(patient_details, patient_report):
    # Create a BytesIO buffer to receive the PDF data.
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=40, bottomMargin=40)

    # Create a list to store the flowables (content) of the PDF.
    story = []

    # Define a style for the report title.
    title_style = getSampleStyleSheet()['Title']
    title_style.alignment = 1  # Center alignment

    # Add the title "Skin Cancer Detection" to the PDF.
    title = Paragraph("<font color=blue>Skin Cancer Detection</font>", title_style)
    story.append(title)
    story.append(Spacer(1, 12))  # Add some space

    # Define a style for the report content.
    normal_style = getSampleStyleSheet()['Normal']

    # Add patient details to the PDF.
    patient_info = f"<b>Name:</b> {patient_details.fname} {patient_details.lname}<br/>" \
                   f"<b>Gender:</b> {patient_details.gender}<br/>" \
                   f"<b>Address:</b> {patient_details.addr}<br/>" \
                   f"<b>Location:</b> {patient_details.location.name}<br/>" \
                   f"<b>Email:</b> {patient_details.email}<br/>" \
                   f"<b>Contact:</b> {patient_details.contact}<br/>" \
                   f"<b>Username:</b> {patient_details.username}"
    patient_info_paragraph = Paragraph(patient_info, normal_style)
    story.append(patient_info_paragraph)
    story.append(Spacer(1, 12))  # Add some space
    if patient_report.image:
        img_path = patient_report.image.path
        img = Image(img_path, width=200, height=150)
        story.append(img)
        story.append(Spacer(1, 12))  # Add some space
    # Add patient report details to the PDF.
    report_info = f"<b>Result:</b> {patient_report.result}<br/>" \
                  f"<b>Time:</b> {patient_report.time}<br/>" \
                  f"<b>Status:</b> {patient_report.status}"
    report_info_paragraph = Paragraph(report_info, normal_style)
    story.append(report_info_paragraph)

    # Build the PDF document.
    doc.build(story)

    # Seek to the beginning of the buffer and return the PDF data.
    buffer.seek(0)
    return buffer


def download_pdf_report(request, report_id):
    # Get the patient report and details
    patient_report_obj = get_object_or_404(patient_report, id=report_id)
    patient_details_obj = patient_report_obj.patient

    # Generate the PDF report
    pdf_buffer = generate_pdf_report(patient_details_obj, patient_report_obj)

    # Create a FileResponse with the PDF data and return it as a downloadable file.
    response = FileResponse(pdf_buffer, as_attachment=True, filename=f'report_{report_id}.pdf')
    return response


