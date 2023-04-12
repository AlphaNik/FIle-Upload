from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from file_upload_app.models import File
from file_upload_app.api.serializers import RegistrationSerializer,FileSerializer
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
                            

@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        if serializer.is_valid():
            user_obj = serializer.save()
            data['username'] = user_obj.username
            data['email'] = user_obj.email
            data['response'] = 'Registration successful'

            token = Token.objects.get(user=user_obj).key
            data['token'] = token

        else:
            data = serializer.errors

        return Response(data,status=status.HTTP_201_CREATED)


@api_view(['POST',])
def logout_view(request):
    print(f'request.user is : {request.user}')
    if request.method == 'POST':
        if request.user.is_anonymous:
            return Response({'error':'No credentials found'},status=status.HTTP_401_UNAUTHORIZED)

        request.user.auth_token.delete()
        return Response({'success':'You have successfully logged out'},status=status.HTTP_200_OK)
    

class AllFileView(ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]


class AllFileByUserView(ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(uploader = user.id)


class FileDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(uploader = user.id)
    

class FileCreateView(CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        user = self.request.user
        serializer.save(uploader=user)