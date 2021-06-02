from django.shortcuts import render
from .models import CustomUser,Courses,Staffs,Subjects,Students
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from  .forms import AddStudentForm,EditStudentForm
from  django.urls import reverse

def admin_home(request):
    return render(request,'hod_template/main_content.html')

def add_staff(request):
    return render(request,'hod_template/add_staff.html')

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        sex = request.POST.get('sex')
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.create_user(email=email, first_name=fname, last_name=lname, username=username,
                                                  password=password, user_type=2)
            user.staffs.address = address
            user.staffs.gender=sex
            user.staffs.profile_pic=profile_pic_url
            user.save()
            messages.success(request,'The staff is added successfully')
            return HttpResponseRedirect(reverse('add_staff'))
        except:
            messages.error(request, 'Failed to add staff')
            return HttpResponseRedirect(reverse('add_staff'))

def add_course(request):
    return render(request,'hod_template/add_course.html')

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_name = request.POST.get('course_name')
        try:
            course = Courses(course_name=course_name)
            course.save()
            messages.success(request,'The course is added successfully')
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, 'Failed to add course')
            return HttpResponseRedirect(reverse('add_course'))

def add_student(request):
    form = AddStudentForm()
    return render(request,'hod_template/add_student.html',{'form':form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            session_start=form.cleaned_data["session_start"]
            session_end=form.cleaned_data["session_end"]
            course_id=form.cleaned_data["course"]
            sex=form.cleaned_data["sex"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.students.address=address
                course_obj=Courses.objects.get(id=course_id)
                user.students.course_id=course_obj
                user.students.session_start_year=session_start
                user.students.session_end_year=session_end
                user.students.gender=sex
                user.students.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "hod_template/add_student.html", {"form": form})

def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,'hod_template/add_subject.html',{'courses':courses, 'staffs':staffs})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)
        print(subject_name,subject_code,staff,course)
        try:
            subject = Subjects(subject_name=subject_name,subject_code=subject_code,course_id=course,staff_id=staff)
            print(subject.subject_name,subject.subject_code,subject.staff_id,subject.course_id)
            subject.save()
            messages.success(request,'The subject is added successfully')
            return HttpResponseRedirect(reverse('add_subject'))
        except:
            messages.error(request, 'Failed to add subject')
            return HttpResponseRedirect(reverse('add_subject'))

def manage_staffs(request):
    staffs = Staffs.objects.all()
    return render(request,'hod_template/manage_staffs.html',{'staffs':staffs})

def manage_students(request):
    students = Students.objects.all()
    return render(request,'hod_template/manage_students.html',{'students':students})

def manage_courses(request):
    courses = Courses.objects.all()
    return render(request,'hod_template/manage_courses.html',{'courses':courses})

def manage_subjects(request):
    subjects = Subjects.objects.all()
    return render(request,'hod_template/manage_subjects.html',{'subjects':subjects})

def edit_staff(request,staff_id):
    staff = Staffs.objects.get(admin_id=staff_id)
    return render(request,'hod_template/edit_staff.html',{'staff':staff, 'id':staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        staff_id = request.POST.get('staff_id')
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        address = request.POST.get('address')
        gender = request.POST.get('sex')
        if request.FILES.get('profile_pic',False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.username = username

            user.save()

            staff = Staffs.objects.get(admin=staff_id)
            staff.address = address
            staff.gender = gender
            if profile_pic_url!=None:
                staff.profile_pic = profile_pic_url
            staff.save()
            messages.success(request,'The staff is edited successfully')
            return HttpResponseRedirect(reverse('edit_staff', kwargs={"staff_id": staff_id}))
        except:
            messages.error(request, 'Failed to edit staff')
            return HttpResponseRedirect(reverse('edit_staff', kwargs={"staff_id": staff_id}))

def edit_student(request,student_id):
    request.session['student_id']=student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.first_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['sex'].initial = student.gender
    form.fields['session_start'].initial = student.session_start_year
    form.fields['session_end'].initial = student.session_end_year

    return render(request,'hod_template/edit_student.html',{'form':form, 'id':student_id})

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.session.get("student_id")
        if student_id == None:
            return HttpResponseRedirect(reverse("manage_student"))

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_start = form.cleaned_data["session_start"]
            session_end = form.cleaned_data["session_end"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES.get('profile_pic',False)
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student = Students.objects.get(admin=student_id)
                student.address = address
                student.session_start_year = session_start
                student.session_end_year = session_end
                student.gender = sex
                course = Courses.objects.get(id=course_id)
                student.course_id = course
                if profile_pic_url != None:
                    student.profile_pic = profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request, "Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))
            except:
                messages.error(request, "Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)
            return render(request, "hod_template/edit_student_template.html",
                          {"form": form, "id": student_id, "username": student.admin.username})

def edit_course(request,course_id):
    print(course_id)
    course = Courses.objects.get(id=course_id)
    return render(request,'hod_template/edit_course.html',{'course':course, 'id':course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')
        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()

            messages.success(request,'The course is edited successfully')
            return HttpResponseRedirect(reverse('edit_course', kwargs={"course_id": course_id}))
        except:
            messages.error(request, 'Failed to edit course')
            return HttpResponseRedirect(reverse('edit_course', kwargs={"course_id": course_id}))
        
def edit_subject(request,subject_id):
    print(subject_id)
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,'hod_template/edit_subject.html',{'subject':subject,'courses':courses,'staffs':staffs, 'id':subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            subject.subject_code = subject_code
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            subject.save()

            messages.success(request,'The subject is edited successfully')
            return HttpResponseRedirect(reverse('edit_subject', kwargs={"subject_id": subject_id}))
        except:
            messages.error(request, 'Failed to edit subject')
            return HttpResponseRedirect(reverse('edit_subject', kwargs={"subject_id": subject_id}))