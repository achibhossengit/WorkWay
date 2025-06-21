from rest_framework.serializers import ModelSerializer
from jobs.models import Job, Detail, Category, Requirement
from users.models import Employer, CustomUser
from rest_framework import serializers

class DetailSerializer(ModelSerializer):
    class Meta:
        model = Detail
        fields = ['description', 'workplace', 'status', 'locations', 'min_salary', 'deadline']

class RequirementSerializer(ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['education', 'experience', 'skill']
        
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class EmployerSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # সরাসরি username যোগ করুন
    class Meta:
        model = Employer
        fields = ['username', 'company', 'location']  # প্রাসঙ্গিক ফিল্ডগুলো ব্যবহার করুন

class JobSerializer(ModelSerializer):
    category = CategorySerializer()
    employer = EmployerSerializer()
    details = DetailSerializer()
    requirements = RequirementSerializer()
    class Meta:
        model = Job
        fields = ['id', 'title', 'employer', 'category', 'published_at', 'details', 'requirements']
        read_only_fields = ['employer']

    def create(self, validated_data):
        details = validated_data.pop('details')
        requirements = validated_data.pop('requirements')
        # set job creator/ employer
        employer = self.context.get('employer')
        validated_data['employer'] = employer
        instance = super().create(validated_data)
        # auto creating details & requirements of this job
        Detail.objects.create(job=instance, **details)
        Requirement.objects.create(job=instance, **requirements)
        return instance
    
    def update(self, instance, validated_data):
        details = validated_data.pop('details')
        requirements = validated_data.pop('requirements')

        details_serializer = DetailSerializer()
        requirements_serializer = RequirementSerializer()
        details_serializer.update(instance.details, details)
        requirements_serializer.update(instance.requirements, requirements)
        
        return super().update(instance, validated_data)
    

class NestedJobSerializer(ModelSerializer):
    details = DetailSerializer()
    requirements = RequirementSerializer()
    class Meta:
        model = Job
        fields = ['id', 'title', 'employer', 'category', 'published_at', 'details', 'requirements']
        read_only_fields = ['employer', 'category']

    def create(self, validated_data):
        details = validated_data.pop('details')
        requirements = validated_data.pop('requirements')
        # set job creator/ employer & category
        validated_data['employer'] = self.context.get('employer')
        validated_data['category'] = self.context.get('category')
        print(validated_data)
        instance = super().create(validated_data)
        # auto creating details & requirements of this job
        Detail.objects.create(job=instance, **details)
        Requirement.objects.create(job=instance, **requirements)
        return instance
    
    def update(self, instance, validated_data):
        details = validated_data.pop('details')
        requirements = validated_data.pop('requirements')

        details_serializer = DetailSerializer()
        requirements_serializer = RequirementSerializer()
        details_serializer.update(instance.details, details)
        requirements_serializer.update(instance.requirements, requirements)
        
        return super().update(instance, validated_data)