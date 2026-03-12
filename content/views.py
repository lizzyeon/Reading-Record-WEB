from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4
from .models import Feed, Like, Reply, Bookmark
from user.models import User
import os
from BOOKSNAP.settings import MEDIA_ROOT


class Main(APIView):    # /main 페이지를 보여줘라
    def get(self, request):                               # 페이지를 열 때(get) 실행되는 함수

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
            feed_user = User.objects.filter(email=feed.email).first()   # 게시물 작성자 정보 가져오기
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
        file = request.FILES.get('file')

        # 파일 이름 생성
        uuid_name = uuid4().hex                          # 랜덤 파일이름 생성
        extension = os.path.splitext(file.name)[1]       # 파일이름과 확장자 분리해서 확장자[1] 가져오기(.jpg .png)
        save_name = uuid_name + extension

        # 'media'에 파일 저장
        save_path = os.path.join(MEDIA_ROOT, save_name)  # 파일 저장 위치 : /project/media/save_name

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():                  # 작은 조각으로 나눠 저장(이미지는 용량이 크기 때문)
                destination.write(chunk)

        image = save_name
        content = request.data.get('content')
        email = request.session.get('email', None)

        # DB 저장
        Feed.objects.create(image=save_name, content=content, email=email)

        # '성공했다'고 브라우저에 알려줌
        return Response(status=200)


class MySnap(APIView):
    def get(self, request):

        email = request.session.get('email', None)       # 로그인할 때 세션에 저장해둔 이메일 가져옴(지금 로그인한 사람 이메일)
        user = User.objects.filter(email=email).first()  # 이메일로 user 조회

        if email is None:
            return render(request, "user/login.html")

        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.filter(email=email).all()
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = Feed.objects.filter(id__in=like_list)
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)

        return render(request, 'content/mysnap.html', context=dict(feed_list=feed_list,
                                                                                like_feed_list=like_feed_list,
                                                                                bookmark_feed_list=bookmark_feed_list,
                                                                                user=user))


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        email = request.session.get('email', None)
        reply_content = request.data.get('reply_content', None)

        Reply.objects.create(feed_id=feed_id, email=email, reply_content=reply_content)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)                      # 좋아요 누른 피드
        email = request.session.get('email', None)                       # 누른 사람
        like = Like.objects.filter(feed_id=feed_id, email=email).first() # 이 피드에, 이 사용자가 좋아요 누른 기록 있는지 확인
                                                                         # filter()은 항상 리스트를 반환하기 때문에 .first필요

        if like is None:                                                     # 이 유저가 좋아요를 누른 적이 없다면
            Like.objects.create(feed_id=feed_id, email=email, is_like=True)  # DB에 새 row 생성
        else:                                                                # 누른 적이 있다면
            like.is_like = not like.is_like                                  # 지금의 반대(not)로 적용해라(좋아요↔취소)
            like.save()                                                      # 변경된 값을 DB에 반영

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