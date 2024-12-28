from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    firstName = models.CharField(max_length=30)
    middleName = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    companyRole = models.CharField(max_length=255)
    lastName = models.CharField(max_length=30)
    country = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=10)

    def __str__(self):
        return "{} {} {} from {}".format(
            self.firstName, self.middleName, self.lastName, self.country)

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company', related_query_name='comp')
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    energyOperationCertificate = models.URLField(max_length=30)
    accNumber = models.CharField(max_length=100)
    bankName = models.CharField(max_length=100)
    
    def __str__(self):
        return "{}".format(self.name)


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', related_query_name='post')
    topic = models.CharField(max_length=1000)
    SOCIALS_CHOICES = (
        ('FACEBOOK', 'FaceBook'),
        ('INSTAGRAM', 'Instagram'),
        ('TWITTER', 'Twitter'),
        ('LINKEDIN', 'LinkedIn'),
        ('THREADS', 'Threads')
    )
    socialsName = models.CharField(max_length=20, choices=SOCIALS_CHOICES)
    content = models.CharField(max_length=100000, blank=True)
    posted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.topic)


class ResearchPapers(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='researchPapers', related_query_name='researchPapers')
    prompt = models.CharField(max_length=30)
    response = models.CharField(max_length=100000, blank=True)

    def __str__(self):
        return "{}".format(self.prompt)
