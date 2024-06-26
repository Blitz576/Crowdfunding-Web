from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from social_auth.serializers import FacebookSocialAuthSerializer


class FacebookSocialAuthView(GenericAPIView):
    serializer_class = FacebookSocialAuthSerializer
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)
