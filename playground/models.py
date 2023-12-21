from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    host        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic       = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    partcipants = models.ManyToManyField(User, related_name="partcipants", blank=True) 
    
    name        = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated','-created']

class Message(models.Model):
    # on_delete makes it so when room is deleted it will do a action on this object. in this case cascade means it will delete itself
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    room        = models.ForeignKey(Room, on_delete=models.CASCADE)

    body        = models.TextField()
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    
import os

class ProfilePic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="Profile_Pics", default='Profile_Pics/Default_Profile_Pic.png')

    def __str__(self):
        return f"Profile Pic for {self.user.username}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # if an element exists
        if self.id is not None:
            current = ProfilePic.objects.get(id=self.id)
            if self.profile_pic != current.profile_pic and os.path.normpath(current.profile_pic.path) != os.path.normpath('C:\\Users\\rayya\\Desktop\\StoreFront\\media\\Profile_Pics\\Default_Profile_Pic.png'):
                # Delete the old image
                current.profile_pic.delete(save=False)    # Set save=False because it's saving now.

        super(ProfilePic, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        # Check if the profile_pic is not the default one
        if os.path.normpath(self.profile_pic.path) != os.path.normpath('C:\\Users\\rayya\\Desktop\\StoreFront\\media\\Profile_Pics\\Default_Profile_Pic.png'):
            # Delete the associated media file
            default_storage.delete(self.profile_pic.name)

        super(ProfilePic, self).delete(using, keep_parents)