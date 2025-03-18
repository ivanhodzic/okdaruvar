from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('startPage',views.startPageView, name='startPageView'),
   path('hometrainer',views.home_trainer_view, name='hometrainer'),
   path('userprofile', views.user_profile_view, name="userprofile"),
   path('userprofileedit', views.user_profile_edit_view, name="userprofileedit"),
   path('changepassword', views.change_password_view, name='changepassword'),
   path('playerstrainer', views.players_trainer_view, name='playerstrainer'),
   path('addplayer', views.add_player_view, name='addplayer'),
   path('saveeditplayer/<int:player_id>', views.save_edit_player_view, name='saveeditplayer'),
   path('editplayer/<int:player_id>', views.edit_player_view, name='editplayer'),
   path('removeplayer/<int:player_id>', views.remove_player, name='removeplayer'),
   path('saveplayer', views.save_player_view, name='saveplayer'),
   path('searchplayer', views.search_player_view, name='searchplayer'),
   path('addplayeronlist/<int:player_id>', views.add_player_on_list_view, name='addplayeronlist'),
   path('trainings', views.trainings_view, name='trainings'),
   path('addreplacemanttraining/<int:trainer_id>', views.add_replacemant_training_view, name='addreplacemanttraining'),
   path('savetraining', views.save_training_view, name='savetraining'),
   path('edittraining/<int:training_id>', views.edit_training_view, name='edittraining'),
   path('saveedittraining/<int:training_id>', views.save_edit_training_view, name='saveedittraining'),
   path('deletetraining/<int:training_id>', views.delete_training_view, name='deletetraining'),
   

] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)