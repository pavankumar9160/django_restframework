from django.db import models

# 

class Skill(models.Model):
   name = models.CharField(max_length=100,blank=True, null=True)

class Student(models.Model):
   
   name = models.CharField(max_length=250,blank=True, null=True)
   age = models.IntegerField()
   email = models.EmailField()
   skills  = models.ManyToManyField(Skill,related_name="students")  # student.objects.all().prefetch_related("skills")
   profile_picture = models.ImageField(upload_to="profile_pictures/",blank=True, null=True)
   
   


   
   
class AdditionalInfo(models.Model):
  
   student = models.OneToOneField(Student, on_delete=models.CASCADE)
   nationality = models.CharField(max_length=250,blank=True, null=True)
   phone_number  = models.CharField(max_length=250,blank=True, null=True)
   
   
class Author(models.Model):
   name = models.CharField(max_length=100,blank=True, null=True)  
   

class Book(models.Model): #related_name = book_set
   title = models.CharField(max_length=100,blank=True, null=True) 
   author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name ="books") # books = books.objects.all().select_related("author")
   


class Candidate(models.Model):
   
   first_name = models.CharField(max_length=100,blank=True,null=True)
   last_name  = models.CharField(max_length=100,blank=True,null=True)
   email =  models.EmailField(max_length=100,blank=True,null=True)
   
   
      
   
   
      
   
   
   

