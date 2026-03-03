from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User

class Join(APIView):
    def get(self,request):
        return render(request, "user/join.html")

    def post(self,request):
        email =  request.data.get('email', None)
        password = request.data.get('password', None)
        name = request.data.get('name', None)
        nickname = request.data.get('nickname', None)

        User.objects.create(email=email,
                            password=make_password(password),
                            name=name,
                            nickname=nickname,
                            profile_image="default_profile.jpg")

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원정보를 다시 한 번 확인해주세요."))

        if user.check_password(password):
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보를 다시 한 번 확인해주세요."))
