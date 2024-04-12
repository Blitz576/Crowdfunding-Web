from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from api.models import User, Category, Project, Rate, ImportantProject
from comment.models import Comment
from replay.models import Replay
from comment_report.models import Report_comment
from Project_Pics.api.serializer import ProjectPicsSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # fields = ["id", "email", "password", "first_name", "last_name", "is_superuser", "is_active", "birth_date", "photo","country","facebook"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        print(type(instance))
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    pics = ProjectPicsSerializer(many=True, read_only=True)
    allrate = RateSerializer(many=True, read_only=True)
    average_rate = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    # def get_allrate(self, obj):
    #     list_rates = list(obj.allrate.values_list('rate', flat=True))
    #     if len(list_rates)>0:
    #         avg = sum(list_rates) / len(list_rates)
    #     else:
    #         avg = 5
    #     print(avg)
    #     return list(obj.allrate.values_list('rate', flat=True))

    def get_average_rate(self, obj):
        list_rates = list(obj.allrate.values_list('rate', flat=True))
        if len(list_rates)>0:
            avg = sum(list_rates) / len(list_rates)
        else:
            avg = 5
        return avg


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class ReplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Replay
        fields = "__all__"

class ReportCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report_comment
        fields = "__all__"


class ImportantProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantProject
        fields = "__all__"