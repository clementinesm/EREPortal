from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class EREAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    DocumentTrackingNumber = models.CharField(max_length=40, blank=True, null=True,unique=True)
    OriginalDocumentID = models.CharField(max_length=40, blank=True, null=True)
    MarketerDUNS = models.CharField(max_length=50, blank=True, null=True)
    UtilityDUNS = models.CharField(max_length=50, blank=True, null=True)
    PaymentDueDate = models.DateField(blank=True, null=True)
    ESIID = models.CharField(max_length=40, blank=True, null=True)
    InvoiceTotalAmount = models.FloatField(blank=True, null=True)
    Processed = models.NullBooleanField()
    updateuser = models.ForeignKey(User, on_delete=models.CASCADE)
    updatedatatime = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'EREAccounts'
        verbose_name_plural = "Enchanted Rock Accounts"

    def __str__(self):
        return 'EREAccounts: {}'.format(self.ESIID)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_level = models.IntegerField(null=False, blank=False, default=0)
    note = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "UserProfile"
        verbose_name_plural = "User Profile Records"

    def __str__(self):
        return 'UserProfile: {}'.format(self.user)

class GraphNames(models.Model):
    id = models.AutoField(primary_key=True)
    url_name = models.CharField(max_length=255, null=True, blank=True)
    long_name =  models.CharField(max_length=255, null=True, blank=True)
    required_access_level = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(null=False,blank=False,default=False)
    displayorder = models.IntegerField(null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "GraphNames"
        verbose_name_plural = "Graph Names"

    def __str__(self):
        return 'GraphNames: {}'.format(self.long_name)


# simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, access_level=-1)
