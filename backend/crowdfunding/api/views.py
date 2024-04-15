from rest_framework.decorators import action
from djoser.compat import get_user_email, settings
from djoser import signals

from api.models import Category, Project, Rate, User, ImportantProject
from api.modelserializers import (
    CategorySerializer,
    CommentSerializer,
    LoginSerializer,
    ProjectSerializer,
    RateSerializer,
    ReplaySerializer,
    UserSerializer, ImportantProjectSerializer, confirmActivation
)
from api.permissions import IsAdminOrReadOnly, IsOwnerProjectOrReadOnly, IsSameUserOrReadOnly
from comment.models import Comment
from comment_report.models import Report_comment
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from replay.models import Replay
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class login(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "is_superuser": user.is_superuser, 
                        "userName": user.first_name + " " + user.last_name })


class UserModelViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsSameUserOrReadOnly]
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        subject = "Confirm account Crowdfunding"
        reset_link = f"http://localhost:8080/congs?uid={uid}&token={token}"
        message = f"welcome to Crowdfunding, to confirm your new account please click on <a href=\"{reset_link}\">Click here</a>"
        from_email = "amr.abdullah.elrefaey@gmail.com"
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])


class CategoryModelViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    # permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

from Project_Pics.api.serializer import ProjectPicsSerializer
from Project_Pics.models import ProjectPics


class ProjectModelViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerProjectOrReadOnly]
    # permission_classes = [AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        project = serializer.save()
        allPhotos = self.request.FILES.getlist('photos')
        for photo in allPhotos:
            newPhoto = ProjectPics()
            newPhoto.image_path=photo
            newPhoto.project=project
            newPhoto.save()

    @action(detail=True, methods=['get'])
    def get_project_photos(self, request, pk=None):
        project = self.get_object()
        photos = ProjectPics.objects.filter(project=project)
        serializer = ProjectPicsSerializer(photos, many=True)
        return Response(serializer.data)


class RateModelViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny]
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class ImportantProjectAPIView(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    # permission_classes = [AllowAny]
    queryset = ImportantProject.objects.all()
    serializer_class = ImportantProjectSerializer


class confirmActivate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = confirmActivation(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data.get('uid')
            token = serializer.validated_data.get('token')
            try:
                uid = str(urlsafe_base64_decode(uid), 'utf-8')
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user and not user.is_active and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({'message': 'Account activated successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


