from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.utils import timezone

class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)
    #used in issue book
    def __str__(self):
        return str(self.user) + "["+str(self.enrollment)+']'
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id

# class category(models.Model):
     
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return str(self.name) 



class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('novel', 'Novel'),
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('scifi','Sci-Fi')
        ]
    name=models.CharField(max_length=500)
    isbn=models.PositiveIntegerField()
    author=models.CharField(max_length=200)
    category=models.CharField(max_length=200,choices=catchoice,default='education')

    def __str__(self):
        return str(self.name) +"["+str(self.isbn)+']'


def get_expiry():
    return datetime.today() + timedelta(days=15)
class IssuedBook(models.Model):
    #moved this in forms.py
    #enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
    # enrollment=models.CharField(max_length=30)
    student = models.ForeignKey(StudentExtra,on_delete=models.SET_NULL,null=True,blank=True)
    #isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
    # isbn=models.CharField(max_length=30)
    book = models.ForeignKey(Book,on_delete=models.CASCADE,null=True,blank=True)
    issuedate=models.DateField(auto_now=False)
    expirydate=models.DateField(default=get_expiry)
    def __str__(self):
        return str(self.student)

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     classroom = models.CharField(max_length=10)
#     branch = models.CharField(max_length=10)
#     roll_no = models.CharField(max_length=3, blank=True)
#     phone = models.CharField(max_length=10, blank=True)
#     image = models.ImageField(upload_to="", blank=True)

#     def __str__(self):
#         return str(self.user) + " ["+str(self.branch)+']' + " ["+str(self.classroom)+']' + " ["+str(self.roll_no)+']'


def expiry():
    return datetime.today() + timedelta(days=14)

class Fine(models.Model):
    student=models.ForeignKey(StudentExtra,on_delete=models.CASCADE)
    issue=models.ForeignKey(IssuedBook,on_delete=models.CASCADE)
    amount=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    paid=models.BooleanField(default=False)
    order_id = models.CharField(unique=True, max_length=500, null=True, blank=True, default=None) 
    datetime_of_payment = models.DateTimeField(auto_now=False,null=True,blank=True)
    
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None :
            self.order_id = "{}_{}_{}".format(self.student.department,self.student.student_id.username,timezone.now().strftime('%H%M%S') )  
        return super().save(*args, **kwargs)

    def __str__(self):
        return "{} fine->{}".format(self.issue,self.amount)



