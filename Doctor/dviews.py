from django.shortcuts import render, redirect
from Doctor.models import DoctorRegistration,DoctorLogin
from Patient.models import PatientRegistration
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd
import codecs
import csv
from Patient.models import PatientAppointment
from django.http import JsonResponse
from csv import reader
from django.contrib.auth.models import User

fs = FileSystemStorage(location='tmp/')


# Serializer
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorRegistration
        fields = "__all__"


# Viewset
class ProductViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Product.
    """
    queryset = DoctorRegistration.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        """Upload data from CSV"""
        file = request.FILES["file"]
        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )
        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        next(reader)
    
        product_list = []
        for id_, row in enumerate(reader):
            (
                doctorid,
                doctorname,
                gender,
                address,
                city,
                mobile,
                specility,
            ) = row
            product_list.append(
                DoctorRegistration(
                    doctorid=doctorid,
                    doctorname=doctorname,
                    gender=gender,
                    address=address,
                    city=city,
                    mobile=mobile,
                    specility= specility,
                    email= doctorname+"@mail.com",
                    rating="5",
                    experience="5",
                )
            )

        DoctorRegistration.objects.bulk_create(product_list)

        return Response("Successfully upload the data")


    @action(detail=False, methods=['POST'])
    def upload_data_with_validation(self, request):
        """Upload data from CSV, with validation."""
        file = request.FILES.get("file")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)

        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        product_list = []
        for row in serializer.data:
            product_list.append(
                DoctorRegistration(
                    doctorid=row[0],
                    doctorname=row[1],
                    gender=row[2],
                    address=row[3],
                    city=row[4],
                    mobile=row[5],
                    specility= row[6],
                )
            )

        DoctorRegistration.objects.bulk_create(product_list)

        return Response("Successfully upload the data")
def Register(request):
    if request.method=='POST':
        if  request.POST['password1']==request.POST['password2'] :
            try:
                DoctorRegistration.objects.get(doctorid=request.POST['userid'])
                return render(request,'DoctorRegistration.html',{'error1':'Userid already exists please choose another Userid '})
            except DoctorRegistration.DoesNotExist:
                try:
                    DoctorRegistration.objects.get(email=request.POST['email'])
                    return render(request,'DoctorRegistration.html',{'error1':'Email already exists please choose another Email '})
                except DoctorRegistration.DoesNotExist:
                    user=request.POST.get('userid')
                    name=request.POST.get('name')
                    email=request.POST.get('email')
                    mobile=request.POST.get('mobile')
                    address=request.POST.get('address')
                    pass1=request.POST.get('password1')
                    city=request.POST.get('city')
                    request.session['user']=user
                    request.session['name']=name
                    request.session['email']=email
                    request.session['mobile']=mobile
                    request.session['address']=address
                    request.session['passsword1']=pass1
                    request.session['city']=city
                    object1=pd.read_csv("Files/Spe_disease.csv")
                    list1=list(set(object1['Specialization']))
                    list1.sort()
                    return render(request,'DoctorRegistration2.html',{'diseases':list1})
        else:
            return render(request,'DoctorRegistration.html',{'error1':'Your passwords does not match Please enter correct Password'})

def Register2(request):
    if request.method=='POST':
        try:
            image=request.FILES.get('file')
            fs=FileSystemStorage()
            fs.save(image.name,image)
            edu=request.POST.get('edu')
            exp=request.POST.get('exp')
            spe=request.POST.get('spe')
            sque=request.POST.get('question')
            sans=request.POST.get('answer')
            insert=DoctorRegistration()
            insert1=DoctorLogin()
            insert.doctorid=request.session['user']
            insert.doctorname=request.session['name']
            insert.email=request.session['email']
            insert.mobile=request.session['mobile']
            insert.address=request.session['address']
            insert.city=request.session['city']
            insert.gender=edu
            insert.experience=exp
            insert.specility=spe
            insert.rating=2.5
            insert.image=image.name
            insert1.doctorid=request.session['user']
            insert1.email=request.session['email']
            insert1.password=request.session['passsword1']
            insert1.status="active"
            insert1.secquestion=sque
            insert1.secanswer=sans
            insert.save()
            insert1.save()
            del request.session['user']
            del request.session['name']
            del request.session['email']
            del request.session['mobile']
            del request.session['address']
            del request.session['passsword1']
            return render(request, 'DoctorLogin.html')
        except DoctorRegistration.DoesNotExist:
            return render(request, 'DoctorRegistration2.html',{'error':'Registration except failed...'})
    else:
        return render(request, 'DoctorRegistration2.html',{'error':'Registration failed...'})


def Login(request):
    if request.method=='POST':
        try:
            obj=DoctorLogin.objects.get(email=request.POST['email'])
            if obj.password==request.POST['password1'] and obj.status=="active":
                id=obj.doctorid
                request.session['did']=id
                obj=DoctorRegistration.objects.get(doctorid=id)
                name=obj.doctorname
                list=name.split(" ")
                request.session['dnm']=list[0]
                return redirect('doctorhome')
            else:
                return render(request, 'DoctorLogin.html', {'error':'Authentication failed...'})
        except DoctorLogin.DoesNotExist:
            return render(request, 'DoctorLogin.html', {'error':'Authentication failed except...'})

def DChangePass(request):
    userid=request.session['did']
    pass1=request.POST.get('pass1')
    pass2=request.POST.get('pass2')
    if(pass2==request.POST.get('pass3')):
        obj=DoctorLogin.objects.get(doctorid=userid)
        if obj.password==pass1:
            obj.password=pass2
            obj.save()
            obj=DoctorRegistration.objects.get(doctorid=userid)
            obj.password=pass2
            obj.save()
            return render(request, 'DoctorChangePassword.html',{'error':'Password Changed Successfully..'})
        else:
            return render(request, 'DoctorChangePassword.html',{'error1':'current password is incorrect'})
    return render(request, 'DoctorChangePassword.html',{'error1':'Password are not same'})




def DoctorProfile(request):
    userid=request.session['did']
    obj=DoctorRegistration.objects.get(doctorid=userid)
    img=obj.image
    dname=obj.doctorname
    mobile=obj.mobile
    email=obj.email
    edu=obj.gender
    exp=obj.experience
    address=obj.address
    spe=obj.specility
    rating=obj.rating
    return render(request,'DoctorProfile.html',{'did':userid,'dnm':dname,'email':email,'mobile':mobile,'edu':edu,'exp':exp,'address':address,'spe':spe,'rating':rating,'error':'disabled','profileimg':img})

def DImage(request):
    if request.method=='POST':
        try:
            image=request.FILES.get('file')
            fs=FileSystemStorage()
            fs.save(image.name,image)
            obj=DoctorRegistration.objects.get(doctorid=request.session['did'])
            eid=obj.doctorid
            DoctorRegistration.objects.filter(doctorid=eid).update(image=image.name)
            return render(request ,'DoctorProfile.html')
        except DoctorRegistration.DoesNotExist:
            return render(request ,'Home.html')


def ForgotPassword(request):
    if request.method=="POST":
        try:
            pass1=request.POST.get('password1')
            pass2=request.POST.get('password2')
            if(pass1==pass2):
                email=request.POST.get('email')
                sque=request.POST.get('squestion')
                sans=request.POST.get('sanswer')
                object1=DoctorLogin.objects.get(email=email)
                if(object1.secquestion==sque and object1.secanswer==sans):
                    object1.password=pass1
                    object1.save()
                    return render(request, 'DoctorForgotPassword.html',{'error':'Password changed successfully please login'})
                else:
                    return render(request, 'DoctorForgotPassword.html',{'error1':'Invalid security question or answer'})
            else:
                return render(request, 'DoctorForgotPassword.html',{'error1':'Password does not match'})
        except DoctorLogin.DoesNotExist:
            return render(request, 'DoctorForgotPassword.html',{'error1':'error'})
        

def AddDisease(request):
    disease=request.POST.get('disease')
    symptom=request.POST.get('symptom')
    object1=pd.read_csv("Files/Disease_and_their_Symptoms.csv")
    data=object1['Diseases'][object1['Diseases']==disease][object1['Symptoms']==symptom].tolist()
    no=len(data)
    if no==0:
        fil=open("Files/Disease_and_their_Symptoms.csv","a",newline='')
        writer=csv.writer(fil)
        writer.writerow([disease,symptom])
        return render(request,'AddDiseaseandSymptom.html',{'message':'Disease and Symptom is added successfully.','link':'Want to add another?'})
    else:
        return render(request,'AddDiseaseandSymptom.html',{'error':'Disease and Symptom already exists please enter another one'})


def DoctorHome2(request):
    datalist=[]
    a=request.GET.get('aid')
    obj=PatientAppointment.objects.filter(doctorid=request.session['did'])
    for i in obj:
        if str(i.id)==a:
            PatientAppointment.objects.filter(id=a).update(appointmentstatus='deleted')
        list1=[]
        if str(i.appointmentstatus)=='Yes':
            list1.append(i.appointdate)
            list1.append(i.patientname)
            list1.append(i.pre_disease)
            print(i.symptoms)
            sym=i.symptoms
            l=sym.replace('[','')
            l1=l.replace(']','')
            l2=l1.replace("'","")
            l3=l2.strip().split(',')
            for j in l3:
                list1.append(j)
            list1.append(i.id)
            datalist.append(list1)
    print(datalist)
    return render(request, 'DoctorHome.html',{'datalist':datalist})

def DoctorHome(request):
    datalist=[]
    doctorid=request.session['did']
    obj=PatientAppointment.objects.filter(doctorid=doctorid).filter(appointmentstatus="Yes")
    for i in obj:
        counter=0
        list1=[]
        id=i.patientid
        patientname=i.patientname
        list1.append(str(i.appointdate))
        list1.append(patientname)
        list1.append(i.pre_disease)
        sym=i.symptoms
        sym=sym[1:-1]
        l3=sym.split(',')
        object1=PatientRegistration.objects.get(patientid=id)
        list1.append(object1.mobile)
        list1.append(object1.email)
        list1.append(i.id)
        for j in l3:
            counter+=1
            if j==l3[0]:
                j=j[1:-1]
                string=str(counter) + " )"+j
                list1.append(string)
            else:
                j=j[2:-1]
                string=str(counter) + " ) "+j
                list1.append(string)
        datalist.append(list1)
        
    return render(request,'DoctorHome.html',{'datalist':datalist})


def TreatedPatient(request):
    pid=request.GET.get('id')
    object1=PatientAppointment.objects.get(id=pid)
    object1.appointmentstatus="treated"
    object1.save()
    return redirect('doctorhome')

def PatientDelete(request):
    pid=request.GET.get('id')
    object1=PatientAppointment.objects.get(id=pid)
    object1.appointmentstatus="No"
    object1.save()
    return redirect('doctorhome')

def DoctorActivity(request):
    datalist=[]
    object1=PatientAppointment.objects.filter(doctorid=request.session['did']).filter(appointmentstatus="treated")
    for obj in object1:
        list1=[]
        counter=0
        list1.append(str(obj.appointdate))
        list1.append(obj.patientname)
        list1.append(obj.pre_disease)
        sym=obj.symptoms
        sym=sym[1:-1]
        l3=sym.split(',')
        for j in l3:
            counter+=1
            if j==l3[0]:
                j=j[1:-1]
                string=str(counter) + " )"+j
                list1.append(string)
            else:
                j=j[2:-1]
                string=str(counter) + " ) "+j
                list1.append(string)
        datalist.append(list1)
    return render(request,'DoctorActivity.html',{'datalist':datalist})




