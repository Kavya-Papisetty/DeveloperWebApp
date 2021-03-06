from pyexpat.errors import messages
from time import timezone
from tkinter.tix import Form
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
from librarymanagementsystem.settings import EMAIL_HOST_USER
from .models import Fine, IssuedBook 
import razorpay
from .utilities import calcFine

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})






def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books=models.Book.objects.all()

    return render(request,'library/viewbook.html',{'books':books})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            # obj=models.IssuedBook()
            # obj.enrollment=request.POST.get('enrollment2')
            # obj.isbn=request.POST.get('isbn2')
            form.save()
            return render(request,'library/bookissued.html')
           

    return render(request,'library/issuebook.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10

            # models.IssuedBook.save()
            
            


        # books=list(models.Book.objects.filter(isbn=ib.isbn))
        # students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        # i=0
        # for l in books:
        #     t=(students[i].user,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine)
        #     i=i+1
        #     li.append(t)
        book_issued = models.IssuedBook.objects.all()

    return render(request,'library/viewissuedbook.html',{'li':li,'issuedbook':book_issued})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    # student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(student__user__id = request.user.id)
    

    li1=[]

    li2=[]
    for ib in issuedbook:
    #     books=models.Book.objects.filter(isbn=ib.isbn)
    
    # for book in books:
    #         t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
    #         li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
    days=(date.today()-ib.issuedate)
    print(date.today())
    d=days.days
    fine=0
    book_issued = models.IssuedBook.objects.all()
    if d>15:
            day=d-15
            fine=day*10
    t=(issdate,expdate,fine)
    li2.append(t)
    book_issued = models.IssuedBook.objects.all()

    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2,'issuedbook':issuedbook})

def aboutus_view(request):
    return render(request,'library/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['wapka1503@gmail.com'], fail_silently = False)
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form':sub})

def delete_book(request,pk):
	book_item = models.Book.objects.get(id=pk)
	if request.method == "POST":
		book_item.delete()
		return redirect('profile')
	context = {'book':book_item,}
	return render(request,'delete.html',context)

def Update(request):
    # if not request.user.is_superuser:
    #     return redirect ('index')
    #obj = Student.objects.get(id=pk)
    form = forms.BookForm(instance=obj)
    if request.method == 'POST':
        form = forms.BookForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            #return redirect(index)
    return render(request, 'library/bookadded.html')
# def edit_profile(request):
#     student = Student.objects.get(user=request.user)

#     form = ProjectForm(instance=student)

#     if request.method == "POST":
#         form = ProjectForm(request.POST, request.FILES)
#         email = request.POST['email']
#         # phone = request.POST['phone']
#         # branch = request.POST['branch']
#         # classroom = request.POST['classroom']
#         # roll_no = request.POST['roll_no']
#         # image = request.POST['image']
#         if form.is_valid():
#             student = form.save(commit=False)
#             student.user.email = email
#         # student.phone = phone
#         # student.branch = branch
#         # student.classroom = classroom
#         # student.roll_no = roll_no
#         # student.image = image
#             student.user.save()
#             student.save()
#             alert = True
#         else:
#             messages.error(request,'Some error occurred')
#         return render(request, "edit_profile.html", {'alert':alert})
    
#     context={'form':form}
#     return render(request, "edit_profile.html",context)


# def Profile(request):
#     return render(request, 'profile.html')

@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser ,login_url='/student/login/')
def myfines(request):
    if models.StudentExtra.objects.filter(student_id=request.user_id):
        student=models.StudentExtra.objects.filter(student_id=request.user_id)[0]
        issues=models.IssuedBook.objects.filter(student=student)
        for issue in issues:
            calcFine(issue)
        fines=Fine.objects.filter(student=student)
        return render(request,'library/myfines.html',{'fines':fines})
    messages.error(request,'You are Not a Student !')
    return redirect('/')


@login_required(login_url='/student/login/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def allfines(request):
    issues=IssuedBook.objects.all()
    for issuebook in issues:
        calcFine(issuebook)
    return redirect('/admin/library/fine/')

@login_required(login_url='/student/login/')
@user_passes_test(lambda u:  u.is_superuser ,login_url='/admin/')
def deletefine(request,fineID):
    fine=Fine.objects.get(id=fineID)
    fine.delete()
    return redirect('/all-fines/')


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser ,login_url='/student/login/')
def payfine(request,fineID):
    fine=Fine.objects.get(id=fineID)
    order_amount = int(fine.amount)*100
    order_currency = 'INR'
    order_receipt = fine.order_id
    
    
    razorpay_order=razorpay_client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, ))
    print(razorpay_order)
    
    
    return render(request,'library/payfine.html',
    {'amount':order_amount,'razor_id':settings.RAZORPAY_KEY_ID,
    'reciept':razorpay_order['id'],
    'amount_displayed':order_amount / 100,
    'address':'a custom address',
    'fine':fine, 
    })


@login_required(login_url='/student/login/')
@user_passes_test(lambda u: not u.is_superuser ,login_url='/student/login/')
def pay_status(request,fineID):
    if request.method == 'POST':
        params_dict={
            'razorpay_payment_id':request.POST['razorpay_payment_id'],
            'razorpay_order_id':request.POST['razorpay_order_id'],
            'razorpay_signature':request.POST['razorpay_signature'],
        }
        try:
            status=razorpay_client.utility.verify_payment_signature(params_dict)
            if status is None:
                fine=Fine.objects.get(id=fineID)
                fine.paid=True
                fine.datetime_of_payment=timezone.now()
                fine.razorpay_payment_id=request.POST['razorpay_payment_id']
                fine.razorpay_signature=request.POST['razorpay_signature']
                fine.razorpay_order_id = request.POST['razorpay_order_id']
                fine.save()
                
            messages.success(request,'Payment Succesfull')
        except:
            messages.error(request,'Payment Failure')
    return redirect('/my-fines/')
