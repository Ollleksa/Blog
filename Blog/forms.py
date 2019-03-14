from django import forms

class NewMessage(forms.Form):
    name = forms.CharField(max_length = 40)
    content = forms.CharField(widget=forms.Textarea(attrs = {'rows': 10, 'cols': 80}))


class NewComment(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs = {'rows': 3, 'cols': 80}))

class NewBlog(forms.Form):
    name = forms.CharField(max_length = 40)