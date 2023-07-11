from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from django.views import View
# from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Post, Comment, HashTag
from .forms import PostForm, CommentForm, HashTagForm
# from django.urls import reverse_lazy, reverse


### Post
class Index(View):
    def get(self, request):
        posts = Post.objects.all()
        # context = 데이터베이스에서 가져온 값
        context = {
            "posts": posts,
            'title': 'Blog'
        }
        return render(request, 'blog/post_list.html', context)
    

class Write(LoginRequiredMixin, View):

    def get(self, request):
        form = PostForm()
        context = {
            'form': form,
            'title': 'Blog'
        }
        return render(request, 'blog/post_form.html', context)
    
    def post(self, request): # request -> HttpRequest 객체
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False) # commit=False 변수 할당만 우선 하고 이후에 수정 가능
            post.writer = request.user
            post.save()
            return redirect('blog:list') # response -> HttpResponse 객체
        context = {
            'form': form
        }
        return render(request, 'blog/post_form.html', context)


class Update(View):
    def get(self, request, pk): # pk는 post_id
        post = Post.objects.get(pk=pk) # <Object: post>
        # get()은 해당 조건이 없을 때 오류를 발생시킨다.
        form = PostForm(initial={'title': post.title, 'content': post.content})
        context = {
            'form': form,
            'post': post,
            'title': 'Blog'
        }
        return render(request, 'blog/post_edit.html', context)
    
    def post(self, request, pk):
        ## try, execpt
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST)

        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('blog:detail', pk=pk) # pk는 post_id
        
        context = {
            'form': form,
            'title': 'Blog'
        }
        return render(request, 'blog/post_edit.html', context)


class Delete(View):
    def post(self, request, pk): # post_id
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('blog:list')
    
    # 클래스 자체에 아예 접근하지 못하게 -> LoginRequiredMixin
    # Login이 되었을 때만 삭제 버튼이 보이게


class DetailView(View):
    def get(self, request, pk): # post_id: 데이터베이스 post_id
        # list -> object 상세 페이지 -> 상세 페이지 하나의 내용
        # pk 값을 왔다갔다, 하나의 인자
        
        # 데이터베이스 방문
        # 해당 글
        # 장고 ORM (pk: 무조건 pk로 작성해야한다.)
        # post = Post.objects.get(pk=pk)
        # # 댓글
        # comments = Comment.objects.filter(post=post)
        # # 해시태그
        # hashtags = HashTag.objects.filter(post=post)
        # print(post)
        
        # 댓글
        # object.objects.select_related('(정)참조 관계를 갖는 필드명').filter(조건)

        # comments = Comment.objects.select_related('post').filter(post__pk=pk)
        # hashtags = HashTag.objects.select_related('post').filter(post__pk=pk)
        
        # comments = Comment.objects.select_related('writer').filter(post=post)
        # comments = Comment.objects.select_related('writer').filter(post__pk=pk) # O
        # comments = Comment.objects.select_related('post') # -> comments[0]
        # comments = Comment.objects.select_related('post').filter(post_id=pk) # O
        # comments = Comment.objects.select_related('post').filter(post__pk=pk) # O
        # comment = Comment.objects.select_related('post').first()

        # 글
        # Object.objects.prefetch_related('역참조필드_set')
        post = Post.objects.prefetch_related('comment_set', 'hashtag_set').get(pk=pk)
        
        comments = post.comment_set.all()
        hashtags = post.hashtag_set.all()

        # 해시태그
        # hashtags = HashTag.objects.select_related('writer').filter(post=post)
        # hashtags = HashTag.objects.select_related('writer').filter(post__pk=pk)
        # hashtags = HashTag.objects.select_related('post')
        # print(comments[0].post.title)
        # for comment in comments:
        #     print(comment.post)
        # <QuerySet[]>
        # value.attr

        # if comments:
        #     post_title = comments[0].post.title
        #     post_content = comments[0].post.content
        #     post_writer = comments[0].post.writer
        #     post_created_at = comments[0].post.created_at
        # else:
        # #     return False
        #     post_title = False
        #     post_content = False
        #     post_writer = False
        #     post_created_at = False
        
        # 댓글 Form
        comment_form = CommentForm()
        
        # 태그 Form
        hashtag_form = HashTagForm()
        
        context = {
            "title": "Blog",
            'post_id': pk,
            'post_title': post.title,
            'post_writer': post.writer,
            'post_content': post.content,
            'post_created_at': post.created_at,
            'comments': comments,
            'hashtags': hashtags,
            'comment_form': comment_form,
            'hashtag_form': hashtag_form,
        }
        
        return render(request, 'blog/post_detail.html', context)


### Comment
class CommentWrite(LoginRequiredMixin, View):
    # def get(self, request):
    #     pass
    '''
    1. LoginRequiredMixin -> 삭제
    2. 비회원 유저 권한 User
    '''
    def post(self, request, pk):
        form = CommentForm(request.POST)
        # 해당 아이디에 해당하는 글 불러옴
        post = Post.objects.get(pk=pk) # <Object: post>
        
        if form.is_valid():
            # 사용자에게 댓글 내용을 받아옴
            content = form.cleaned_data['content']    
            # 유저 정보 가져오기
            writer = request.user
            # 댓글 객체 생성, create 메서드를 사용할 때는 save 필요 없음
            try:
                comment = Comment.objects.create(post=post, content=content, writer=writer)
                # 생성할 값이 이미 있다면 오류 발생, Unique 값이 중복될 때
                # 필드 값이 비어있을 때: ValidationError
                # 외래키 관련 데이터베이스 오류 : ObjectDoesNotExist
                # get_or_create() -> 2가지 경우의 리턴값
                # comment, created = Comment.objects.get_or_create(post=post, content=content, writer=writer)
                # if created: print('생성되었습니다.') else: print('이미 있습니다.')
                # comment = Comment(post=post) -> comment.save()
            except ObjectDoesNotExist as e:
                print('Post does not exist', str(e))
            except ValidationError as e:
                print('Validation error occurred', str(e))

            return redirect('blog:detail', pk=pk)
        
        hashtag_form = HashTagForm()

        context = {
            "title": "Blog",
            'post_id': pk,
            'comments': post.comment_set.all(),
            'hashtags': post.hashtag_set.all(),
            'comment_form': form,
            'hashtag_form': hashtag_form
        }
        return render(request, 'blog/post_detail.html', context)


class CommentDelete(View):
    def post(self, request, pk): # comment_id
        # 지울 객체를 찾아야 한다. -> 댓글 객체
        comment = get_object_or_404(Comment, pk=pk)

        post_id = comment.post.id
        # 삭제
        comment.delete()
        
        return redirect('blog:detail', pk=post_id)


### Tag
class HashTagWrite(LoginRequiredMixin, View):

    def post(self, request, pk): # pk는 post_id
        form = HashTagForm(request.POST)
        post = get_object_or_404(Post, pk=pk)

        if form.is_valid():
            # 사용자에게 태그 내용을 받아옴
            name = form.cleaned_data['name']
            # 작성자 정보 가져오기
            writer = request.user

            # 댓글 객체 생성, create 메서드를 사용할 때는 save 필요 없음
            try:
                hashtag = HashTag.objects.create(post=post, name=name, writer=writer)
            except ObjectDoesNotExist as e:
                print('Comment does not exist', str(e))
            except ValidationError as e:
                print('Validation error occurred', str(e))

            return redirect('blog:detail', pk=pk)
        
        # form.add_error(None, '폼이 유효하지 않습니다.')
        comment_form = CommentForm()

        context = {
            'title': 'Blog',
            'post': post,
            'comments': post.comment_set.all(),
            'hashtags': post.hashtag_set.all(),
            'comment_form': comment_form,
            'hashtag_form': form
        }

        return render(request, 'blog/post_detail.html', context)


class HashTagDelete(View):

    def post(self, request, pk): # pk는 hashtag_id
        # 지울 객체를 찾아야 한다. -> 태그 객체
        hashtag = get_object_or_404(HashTag, pk=pk)
        # 상세페이지로 돌아가기
        post_id = hashtag.post.id
        # 삭제
        hashtag.delete()
        
        return redirect('blog:detail', pk=post_id)