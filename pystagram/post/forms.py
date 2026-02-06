from django.forms import inlineformset_factory

from post.models import  Post, PostImage, Comment
from utils.forms import BootstrapModelForm


class PostForm(BootstrapModelForm):
    class Meta:
        model = Post
        fields = ('content', )


class PostImageForm(BootstrapModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)


PostImageFormSet = inlineformset_factory(
    Post, PostImage, form=PostImageForm, extra=1, can_delete=True
)
# extra는 추가할 자식 폼의 수를 설정, can_delete 폼의 삭제 여부를 설정
# min_num, max_num 설정은 최소 저장 수와 최대 저장수를 설정하여 최대수를 넘기면 이미지는 들어가지만 저장은 안된다
# form은 formset의 forms 로 사용이 가능하며 forms에 visible_fields 인풋 박스를 설정하며 지금은 이미지 선택이 출력된다
# form -> formaset=[PostImageForm(),PostImageForm()] 식으로 만들어짐
# inlineformset_factory 첫번째는 위에 PostImageForm() 부분에 PostImageForm(post=post) 식으로 넣어준다
# 부모 모델의 인스턴스를 편집할 때 자식 모델의 인스턴스도 함께 관리할 수 있는 폼셋을 자동으로 생성

formset = [
    PostImageForm(),
    PostImageForm(),
    PostImageForm(),
]

class CommentForm(BootstrapModelForm):
    class Meta:
        model = Comment
        fields = ('content', )