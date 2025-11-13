from rest_framework import serializers

from .models import *



        
        
        
class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields= ["id","title"]
    
        

class AuthorSerializer(serializers.ModelSerializer):
    
    books_data = BookSerializer(many=True,source="books")
    
    class Meta:
        model = Author
        fields= ['id','name',"books_data"]
        
    
    def create(self,validated_data):
        
        print("validated_data",validated_data)
        
        books_data = validated_data.pop('books',[])
        
        print("books_data",books_data)
        
        name = validated_data.get("name")
        
        author = Author.objects.create(name=name)
        
        for book_data in books_data:
            
            print("title",book_data.get('title'))
                        
            Book.objects.create(author=author,title=book_data.get('title'))
            
            
        return  author   
    
 
    
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']
    

class StudentSerializer(serializers.ModelSerializer):
    
    skills_data =SkillSerializer(many=True,source="skills")
    
    
    
    class Meta:
        model = Student
        fields = ['name','age','email','skills_data','profile_picture'] 
        
    def create(self,validated_data):
        
        
        skills_data = validated_data.pop('skills',[])
        
        student = Student.objects.create(**validated_data)
        skill_obj=[]    
        for skill_data in skills_data:
            obj,created=Skill.objects.get_or_create(name=skill_data.get("name") )
            skill_obj.append(obj)
        student.skills.set(skill_obj)
        
        student.save()
        return student
    
    def update(self,instance,validated_data):
        skills_data = validated_data.pop('skills_data',[])
        
        skill_obj=[]
        for skill_data in skills_data:
            obj,created=Skill.objects.get_or_create(name=skill_data.get("name") )
            skill_obj.append(obj)
            
        instance.skills.set(skill_obj)
        instance.save()
        return instance
    

class get_student_record_serializer(serializers.ModelSerializer):
    
    skills= serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ['id','name','age','email','skills','profile_picture']
        
        
    def get_skills(self,obj):
        return [skill.name  for skill in obj.skills.all()]
    
    
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Candidate
        fields="__all__"            
        
        
        
        
        
            
        
        
        
    
            
        
  
            
    
   
       
       
        
        
        
            
        

            
        

        