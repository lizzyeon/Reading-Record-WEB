from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4
from .models import Feed, Like, Reply, Bookmark
from user.models import User
import os
from BOOKSNAP.settings import MEDIA_ROOT


class Main(APIView):    # /main 페이지를 보여줘라
    def get(self, request):                                        # 페이지를 열 때(get) 실행되는 함수

        # user 정보를 편하게 사용하기 위함(프로필 등에)
        email = request.session.get('email', None)        # 로그인할 때 세션에 저장해둔 이메일 가져옴(지금 로그인한 사람 이메일)
        user = User.objects.filter(email=email).first()   # 이메일로 user 조회

        # 로그인 정보가 없으면 로그인 화면으로 이동(세션에 email 없거나, DB에 user 없을 시)
        if email is None:
            return render(request, "user/login.html")

        if user is None:
            return render(request, "user/login.html")

        feed_object_list = Feed.objects.all().order_by('-id')      # feed 테이블의 모든(all) 데이터(objects)를 가져옴.
                                                                   # id 기준 내림차순(최신 글이 위로)
                                                                   # SELECT * FROM content_feed ORDER BY id DESC; 와 동일
        # 피드 구성
        feed_list = []       # feed, user, reply 등 데이터를 하나로 묶어 담을 리스트. 이것들이 합쳐서 하나의 피드를 만듦

        for feed in feed_object_list:
            feed_user = User.objects.filter(email=feed.email).first()        # 게시물 작성자 정보 가져오기
            reply_object_list = Reply.objects.filter(feed_id=feed.id)   # 이 게시물에 달린(feed_id가 같은) 댓글 가져오기

            # 댓글 구성
            reply_list = []

            for reply in reply_object_list:
                reply_user = User.objects.filter(email=reply.email).first()

                # 댓글 구성 요소(누가, 어떤 댓글을 달았다)
                reply_list.append(dict(nickname=reply_user.nickname, reply_content=reply.reply_content))

            # 좋아요 처리
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()             # 좋아요 총 개수
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists() # 사용자의 좋아요 누름 여부
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            # feed_list(하나의 피드) 구성 요소
            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=feed_user.profile_image,
                                  nickname=feed_user.nickname,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked))

        user = User.objects.filter(email=email).first()  # 이메일로 user 조회

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
        content = request.data.get('content')
        email = request.session.get('email', None)

        # DB 저장
        Feed.objects.create(image=image, content=content, email=email, like_count=0)

        # '성공했다'고 브라우저에 알려줌
        return Response(status=200)


class MySnap(APIView):
    def get(self, request):

        email = request.session.get('email', None)  # 로그인할 때 세션에 저장해둔 이메일 가져옴(지금 로그인한 사람 이메일)
        user = User.objects.filter(email=email).first()  # 이메일로 user 조회

        if email is None:
            return render(request, "user/login.html")

        if user is None:
            return render(request, "user/login.html")

        return render(request, 'content/mysnap.html', context=dict(user=user))


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        email = request.session.get('email', None)
        reply_content = request.data.get('reply_content', None)

        Reply.objects.create(feed_id=feed_id, email=email, reply_content=reply_content)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        email = request.session.get('email', None)
        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like is None:
            Like.objects.create(feed_id=feed_id, email=email, is_like=True)
        else:
            like.is_like = not like.is_like
            like.save()

        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        email = request.session.get('email', None)
        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark is None:
            Bookmark.objects.create(feed_id=feed_id, email=email, is_marked=True)
        else:
            bookmark.is_marked = not bookmark.is_marked
            bookmark.save()

        return Response(status=200)