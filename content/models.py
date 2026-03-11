from django.db import models

# 피드
class Feed(models.Model):
    content = models.TextField()                    # 글 내용
    image = models.TextField()                      # 피드 이미지
    email = models.EmailField(default='')           # 글쓴이

# 좋아요
class Like(models.Model):
    feed_id = models.IntegerField(default=0)        # 몇 번 피드에 대해서(어떤 피드에 대해서)
    email = models.EmailField(default='')           # 좋아요 누른 사람(email에 저장된 user 활용)
    is_like = models.BooleanField(default=True)     # 좋아요를 취소하면 update(delete가 아닌 T ↔ F)

# 댓글
class Reply(models.Model):
    feed_id = models.IntegerField()                 # 몇 번 피드에 대해서
    email = models.EmailField(default='')           # 댓글 쓴 사람
    reply_content = models.TextField()              # 댓글 내용

# 북마크
class Bookmark(models.Model):
    feed_id = models.IntegerField()                 # 몇 번 피드에 대해서
    email = models.EmailField(default='')           # 북마크 한 사람
    is_marked = models.BooleanField(default=True)   # 북마크 취소하면 update(T ↔ F)