from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.dispatch import receiver


# Create your models here.


class Club(models.Model):
    club_name = models.CharField(max_length=100)
    oib = models.CharField(max_length=11)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    iban = models.CharField(max_length=35)
    logo = models.ImageField(blank=True,upload_to='images/logos/')
    
    def __str__(self):
        return self.club_name


    
class Trainer(models.Model):
    club = models.ForeignKey(Club, null=True, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    mobile = models.CharField(max_length=30,default=None, blank=True, null=True)
    image = models.ImageField(blank=True,upload_to='images/trainers/')

    #Return date formated like 1.1.2001 without leading zeroes
    def get_formated_bithday(self):
        return self.birthday.strftime("%e.%#m.%Y")
    
    #Return date formated like 2001.01.01 with leading zeroes
    def get_formated_bithday2(self):
        return self.birthday.strftime('%Y-%m-%d')

    def __str__(self):
        return f"{self.user}"
    

class MembershipFeeType(models.Model):
    name = models.CharField(max_length=20)
    membership_fee = models.DecimalField(max_digits=5,decimal_places=2)
    def __str__(self):
        return f"{self.membership_fee} €"

class MembershipFee(models.Model):   
    date = models.DateField()
  
    def __str__(self):
        return f"{self.date.month} | {self.date.year}"

class Player(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.PROTECT, null=True)
    membership_fee_type = models.ForeignKey(MembershipFeeType, on_delete=models.PROTECT, null=True)
    membership_fees = models.ManyToManyField(MembershipFee,through='PlayersHasMembershipFee')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    oib = models.CharField(max_length=11,unique=True)
    birthday = models.DateField()
    father_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=30, default=None, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='images/players/')
    access_card = models.ImageField(blank=True, upload_to='images/playersAccessCards/')
    cartificate_of_nationality = models.ImageField(blank=True, upload_to='images/certificatesOfNationality/')
    medical_examination = models.DateField(blank=True, null=True)
   
    def get_formated_bithday(self):
        return self.birthday.strftime("%e.%#m.%Y")
   
    def __str__(self):
        return f"{self.user}"

class Training(models.Model):
    TRANING_DURATIONS = [
        (1,'1h'),
        (1.5,'1.5h'),
        (2,'2h'),
        (2.5,'2.5h'),
        (3,'3h')
    ]

    trainer = models.ForeignKey(Trainer, on_delete=models.PROTECT)
    players = models.ManyToManyField(Player, through='TrainingHasPlayers')
    date = models.DateField()
    replacement = models.ForeignKey(Trainer, on_delete=models.PROTECT,blank=True, related_name='replacement_trainings', null=True)
    training_duration = models.DecimalField(max_digits=2,decimal_places=1, choices=TRANING_DURATIONS)
    comment = models.TextField(blank=True)
    def __str__(self):
        return f"{self.trainer} {self.date} {self.training_duration}h"

class TrainingHasPlayers(models.Model):
    REASONS_OF_ABSENCE = [
        ('Bez razloga','Bez razloga'),
        ('Škola','Škola'),
        ('Bolest','Bolest')
    ]

    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    presence = models.BooleanField()
    absence_reason =  models.CharField(max_length=30, choices=REASONS_OF_ABSENCE, blank=True )
    
    def __str__(self):
        return f"{self.player} {self.training} {self.presence}"
    
    class Meta:
        unique_together=('player','training')

class PlayersHasMembershipFee(models.Model):
    player = models.ForeignKey(Player,on_delete=models.PROTECT)
    membership_fee = models.ForeignKey(MembershipFee, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=5,decimal_places=2)
    def __str__(self):
        return f"{self.player} {self.membership_fee} {self.amount}"    



@receiver(models.signals.pre_save, sender=Trainer)
def delete_old_image_Trainer(sender, instance, **kwargs):
    if instance.pk:
        # Ako objekt ima primarni ključ, znači da se ažurira
        try:
            # Dohvati trenutno stanje objekta iz baze podataka
            old_instance = sender.objects.get(pk=instance.pk)
            # Usporedi staru sliku i novu sliku
            if old_instance.image != instance.image:
                # Ako se slike razlikuju, izbriši staru sliku
                old_instance.image.delete(save=False)
        except sender.DoesNotExist:
            pass

@receiver(models.signals.pre_save, sender=Player)
def delete_old_image_Player(sender, instance, **kwargs):
     if instance.pk:
        # Ako objekt ima primarni ključ, znači da se ažurira
        try:
            # Dohvati trenutno stanje objekta iz baze podataka
            old_instance = sender.objects.get(pk=instance.pk)
            # Usporedi staru sliku i novu sliku
            if old_instance.image != instance.image:
                # Ako se slike razlikuju, izbriši staru sliku
                old_instance.image.delete(save=False)
             # Usporedi staru karticu i novu karticu
            if old_instance.access_card != instance.access_card:
                # Ako se kartice razlikuju, izbriši staru karticu
                old_instance.access_card.delete(save=False)
            if old_instance.cartificate_of_nationality != instance.cartificate_of_nationality:
                # Ako se kartice razlikuju, izbriši staru karticu
                old_instance.cartificate_of_nationality.delete(save=False)
        except sender.DoesNotExist:
            pass
