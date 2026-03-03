from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4
from .models import Feed
from user.models import User
import os
from BOOKSNAP.settings import MEDIA_ROOT


class Main(APIView):    # Main을 처리하는 view
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id')      # feed 테이블의 모든(all) 데이터(objects)를 가져옴.
                                                            # id 기준 내림차순(최신 글이 위로)
                                                            # SELECT * FROM content_feed ORDER BY id DESC;  와 동일
        # user 정보를 편하게 사용하기 위함(프로필 등에)
        email = request.session.get('email')                # 로그인할 때 세션에 저장해둔 이메일 가져옴(지금 로그인한 사람 이메일)
        user = User.objects.filter(email=email).first()     # 이메일로 user 조회

        # 로그인 정보가 없으면 로그인 화면으로 이동(세션에 email 없거나, DB에 user 없을 시)
        if email is None:
            return render(request, "user/login.html")

        if user is None:
            return render(request, "user/login.html")

        # 정상 로그인 상태면 Main 렌더링
        return render(request, "BOOKSNAP/MAIN.html", {"feeds": feed_list, "user" : user})


class UploadFeed(APIView):
    def post(self, request):

        # 데이터 꺼내기
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        # ('media'에) 파일 저장
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content= request.data.get('content')
        user_id= request.data.get('user_id')
        profile_image= request.data.get('profile_image')

        # DB 저장
        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=0)

        # '성공했다'고 브라우저에 알려줌
        return Response(status=200)
    

