from django.shortcuts import render, redirect

from rest_framework import generics, mixins

from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework import status




from .serializers import *
# Create your views here.

    

     
 
class get_student_record(APIView) :    
   
   def post(self,request):
      
      id = request.data.get("id")
      
      student = Student.objects.get(id=id)
      data={
         
         "name":student.name,
         "age": student.age,
         "email": student.email,
         "additional_info":{
            
             "nationality": student.additionalinfo.nationality,
         "phone_number": student.additionalinfo.phone_number,

         }
        
         
      }
      return Response(data)
   
   

class update_record(APIView):
   
   def put(self,request):
   
      id = request.data.get("id")
         
      student = Student.objects.get(id=id)
      serializer = UpdateStudentSerializer(student,data=request.data,partial=True)
      if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
      return Response(serializer.errors)
   
   
   

class create_author_record(APIView):
     
     def post(self,request):
        
        name = request.data.get("name")
        books_data = request.data.get("books",[])
        
        author = Author.objects.create(name=name)
        
        for book_data in books_data:
           Book.objects.create(author=author,title=book_data.get("title"))
        
        
        return Response({"message":"record created"}) 
     
     

     def get(self,request):
        
        
         authors = Author.objects.all().prefetch_related("books")  
         
         data=[]
         
         for author in authors:
            
            data.append({
               "name": author.name,
               "books":[{
                  "id":book.id,
                  "title":book.title
               }
                  
                  for book in author.books.all()
                  
                  
               ]
            })
          
         return Response(data)   


class get_author_records(APIView):
   
   def get(self,request):
      
      authors = Author.objects.all()
      serializer = AuthorSerializer(authors,many=True)    
      return Response(serializer.data)
   
   
   def post(self,request):
      
      serializer = AuthorSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save() # create or update
         return Response(serializer.data)
      return Response(serializer.errors)
   


class update_author_record(APIView):   
   
   
   def put(self,request):
      
      id = request.data.get("id")
      books_data = request.data.get("books_data",[])
      author = Author.objects.get(id=id)
      
      for book_data in books_data:
        book_id =  book_data.get("id")
        book_title = book_data.get("title")
        
        book_obj = Book.objects.get(author=author,id=book_id)
        
        book_obj.title = book_title
        book_obj.save()
        
        
        
      
      return Response({"message":"record updated successfully"})  
   
   
from rest_framework import parsers

#this is view is for creating a student record
class create_student_record(APIView):   
   
   parser_classes = [parsers.MultiPartParser, parsers.FormParser]  

   def post(self, request):
      data = request.data.copy()  # QueryDict → mutable dict

      # Parse skills_data JSON string if it exists
      if 'skills_data' in data and isinstance(data['skills_data'], str):
         import json
         data['skills_data'] = json.loads(data['skills_data'])

      serializer = StudentSerializer(data=data)
      
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors)
   
   


class get_student_record(APIView):
   def get(self,request):
      students  = Student.objects.all()
      
      serializer = get_student_record_serializer(students,many=True)
     
      return Response(serializer.data)
   
   

class update_student_record(APIView):   
   
   
   def put(self,request):
      
      id = request.data.get("id")
      student = Student.objects.get(id=id)
      
      serializer = StudentSerializer(student,data=request.data,partial=True)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors)
   
   

#mixins->ListModel,createModel,retrieveModel,UpdateModel,DrestroyModel 



class CandidateCreateView(mixins.CreateModelMixin,mixins.ListModelMixin,generics.GenericAPIView):
   
   queryset = Candidate.objects.all() 
   serializer_class = CandidateSerializer
   
   def post(self,request):
      return self.create(request)
   
   def get(self,request):
      return self.list(request)
   

class CandidateDetailView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
   
   queryset = Candidate.objects.all() 
   serializer_class = CandidateSerializer
   
   def get(self,request,pk):
      return self.retrieve(request,pk)
   
   def put(self,request,pk):
      return self.update(request,pk)
   
   def delete(self,request,pk):
      return self.destroy(request,pk)
   

def CandidatePage(request):
   
   candidates = Candidate.objects.all()
   
   
   return render(request,'candidate.html',{"candidates":candidates})   
      
     
class GetAllCandidates(APIView):
   
    def get(self,request):
      candidates  = Candidate.objects.all()
      
      serializer = CandidateSerializer(candidates,many=True)
     
      return Response(serializer.data)

from .forms import CandidateForm   

def AddStudentPage(request):
   
   if request.method =="POST":
      
      form = CandidateForm(request.POST)
      
      if form.is_valid():
         form.save()
         return redirect('homepage')
   else :
      
      form = CandidateForm()   
   
   return render(request,'addstudent.html',{'form':form})        
      
      
def EditCandidate(request,id):
   
   candidate = Candidate.objects.get(id=id)
   
   if request.method =="POST":
      
      candidate.first_name = request.POST.get("firstname")
      candidate.last_name = request.POST.get("lastname")
      candidate.email = request.POST.get("email")
      candidate.save()
      return redirect("homepage")
      
   
   return render(request,"edit-candidate.html",{'candidate':candidate})



def DeleteCandidate(request,id):
   
   candidate = Candidate.objects.get(id=id)
   candidate.delete()
   
   return redirect("homepage")


from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout


from django.contrib.auth.decorators import login_required

def signupView(request):
   
   if request.method=="POST":
      
      first_name = request.POST.get("firstname")
      last_name = request.POST.get("lastname")
      email = request.POST.get("email")
      username= request.POST.get('username')
      password= request.POST.get('password')
      
      user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,
                                      email=email,password=password)
      
      return redirect('login')
      
      

      
      
   

   return render(request,'signup.html')




def loginView(request):
   
   if request.method=="POST":
      
      username= request.POST.get('username')
      password= request.POST.get('password')
      
      user = authenticate(request,username=username,password=password)
      
      if user is not None:
            login(request,user)
            return redirect('CandidatePage')
         
      else:
         return redirect("signup")
   
   
   

   return render(request,'login.html')



def logoutView(request):
   logout(request)
   return redirect("login")
   
   
   
   
   
         
      
      
      
      
      
      
      
      
      
@login_required
def CandidatePage(request):
   
   candidates = Candidate.objects.all()
   
   if request.method=="POST":
      
      candidate_id = request.POST.get("candidate_id") 
      first_name = request.POST.get("firstname")
      last_name = request.POST.get("lastname")
      email = request.POST.get("email")
      
      if candidate_id:
         
         candidate = Candidate.objects.get(id=candidate_id)
      
         candidate.first_name = first_name
         candidate.last_name = last_name
         candidate.email = email
         candidate.save()
      
      else:   
      
         Candidate.objects.create(first_name=first_name,last_name=last_name,email=email)
      return redirect("CandidatePage")
   
   
   edit_id = request.GET.get("edit") 
   candidate_edit = None
   
   if edit_id:
      candidate_edit = Candidate.objects.get(id=edit_id)
   
      
   delete_id = request.GET.get("delete") 
   if delete_id:
      candidate_delete = Candidate.objects.get(id=delete_id)
      candidate_delete.delete()
      return redirect("CandidatePage")
         
   return render(request,'candidate.html',{"candidates":candidates ,'candidate_edit':candidate_edit})         



        
      
      
      
            
            
            
        
        
        
        
         
        
         
   
   
   
      
      
      
      
      
      

        

        
        
            
            
         
         
         
         
         
 


      
    
    
        
    
    
        
    

    
        
               
        
        
            
            
        
        
        
        
    
    
    
    
    
