from django import forms
from todo.models import Todo, Comment


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = (
            'title',
            'description',
            'start_date',
            'end_date',
            'is_completed'
        )
        widgets = {
            'start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'end_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            )
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'message',
        )
        labels = {
            'message': '내용'
        }
        widgets = {
            'message': forms.Textarea(
                attrs={
                    'rows': 3,
                    'cols': 30,
                    'class': 'form-control',
                    'placeholder': '내용을 입력하세요'
                }
            )
        }