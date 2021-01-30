from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',) # Comment모델에서 content만 폼으로 불러온다는 뜻이다. 템플릿에 content 모델만 출력된다.
                                #fields대신 exclude를 쓸 수 있다. exclude는 제외할 모델을 선택한다. 그 모델 말고는 모든 모델을 폼으로 불러온다는뜻이다. 
                                # 자세한 내용은 475쪽 476쪽 참조.