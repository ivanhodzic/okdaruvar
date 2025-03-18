from django.contrib import admin
from  . models import Club, Trainer, Player, Training, TrainingHasPlayers, MembershipFee, MembershipFeeType, PlayersHasMembershipFee
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

# Register your models here.

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    pass

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user','players')

    def players(self, obj:Trainer):
        number_of_players = Player.objects.filter(trainer=obj).count()
        url = (
            reverse('admin:trainings_player_changelist')
            +f"?trainer__id__exact={obj.pk}"
        )
        return format_html('<a href="{}">{} Players</a>', url, number_of_players)
    


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user','trainer')
    

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'date', 'training_duration','number_of_players', 'number_of_absence_players','replacement')
    list_filter = ('trainer',)
    search_fields = ['date']
    
    def number_of_players(self, obj:Training):
        players = TrainingHasPlayers.objects.filter(training=obj)

        url = (
            reverse('admin:trainings_traininghasplayers_changelist')
            +f"?training__id={obj.pk}"
        )
        return format_html('<a href="{}">{} Players</a>', url, players.count())
    
    def number_of_absence_players(self, obj):
        players = TrainingHasPlayers.objects.filter(training=obj,presence=False)
        url = (
            reverse('admin:trainings_traininghasplayers_changelist')
            +f"?training__id={obj.pk}&presence=False"
        )
        return format_html('<a href="{}">{} Players</a>', url, players.count())

@admin.register(TrainingHasPlayers)
class TrainingHasPlayersAdmin(admin.ModelAdmin):
   list_display = ('trainer','player','date','duration', 'presence')
   
   def trainer(self,obj: TrainingHasPlayers):
       return obj.training.trainer
   def date(self,obj: TrainingHasPlayers):
       return obj.training.date
   def duration(self,obj: TrainingHasPlayers):
       return f"{obj.training.training_duration}h"
        
@admin.register(MembershipFee)
class MembershipFeeAdmin(admin.ModelAdmin):
    pass

@admin.register(MembershipFeeType)
class MembershipFeeTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(PlayersHasMembershipFee)
class PlayersHasMembershipFeeAdmin(admin.ModelAdmin):
    list_display = ('player','membership_fee','amount')