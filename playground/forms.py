from django.forms import ModelForm
from .models import Topic, Room, Message, ProfilePic
from django.contrib.auth.models import User

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ProfilePicForm(ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['profile_pic']