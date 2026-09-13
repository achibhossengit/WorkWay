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
    id = serializers.IntegerField(source='user_id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Employer
        fields = ['id', 'username', 'company', 'location']

class JobSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
    )
    employer = EmployerSerializer(read_only=True)
    details = DetailSerializer()
    requirements = RequirementSerializer()

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'employer',
            'category',
            'category_id',
            'published_at',
            'details',
            'requirements',
        ]
        read_only_fields = ['employer', 'published_at']

    def create(self, validated_data):
        details = validated_data.pop('details')
        requirements = validated_data.pop('requirements')
        employer = self.context.get('employer')
        if not employer:
            raise serializers.ValidationError('Only employers can post jobs.')
        validated_data['employer'] = employer
        instance = super().create(validated_data)
        Detail.objects.create(job=instance, **details)
        Requirement.objects.create(job=instance, **requirements)
        return instance

    def update(self, instance, validated_data):
        details = validated_data.pop('details', None)
        requirements = validated_data.pop('requirements', None)

        if details is not None:
            DetailSerializer().update(instance.details, details)
        if requirements is not None:
            RequirementSerializer().update(instance.requirements, requirements)

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