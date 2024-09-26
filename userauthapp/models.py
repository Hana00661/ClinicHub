from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPE = (       #choices if the user is a doctor or patient
    ("Doctor", "Doctor"),
    ("Patient", "Patient"),
)

class User(AbstractUser):       # override default user model
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, null=True, blank=True, default=None)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username    #string representation of the object
    
    def save(self, *args, **kwargs):        #override the default save method to Extracting Username from Email , Conditional Username Assignment and Calling the Inherited save()
        email_username, _ = self.email.split("@")       #split the email address into username and domain
        if self.username == "" or self.username == None: #if username is empty, set it to the email username that means the user dont give us a usre name, we will use the email username as the username
            self.username = email_username
        
        super(User, self).save(*args, **kwargs)    #self.save() did not work with me when i had to override the default save method, so i save it as django way
