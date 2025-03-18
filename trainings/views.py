from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import Trainer, MembershipFeeType, User, Player, Training, TrainingHasPlayers
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
import re
import string
import secrets
from datetime import datetime,date
from django.db import IntegrityError


def startPageView(request):
    trainers = Trainer.objects.all()
    context = {
        'trainers': trainers,  
    }
    return render(request,'startPage.html',context)

@login_required(login_url='/')
def home_trainer_view(request):
    trainer = Trainer.objects.get(user=request.user)

    context = {
        'title': "User profile", 
        'trainer': trainer 
    }
    return render(request,'homeTrainer.html',context )

"""
def home(request):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request,'home.html' )

"""
@login_required(login_url='/')
def user_profile_view(request):

    trainer = Trainer.objects.get(user=request.user)

    context = {
        'title': "User profile", 
        'trainer': trainer 
    }
    return render(request,'userprofile.html',context )

@login_required(login_url='/')
def user_profile_edit_view(request):

    trainer = Trainer.objects.get(user=request.user)
    
    if request.method == 'POST':
        user = trainer.user
        user.first_name = request.POST['inputFirstName']
        user.last_name = request.POST['inputLastName']
        user.email= request.POST['inputEmail']
        user.save()
        trainer.birthday = request.POST['inputBirthday']
        trainer.mobile = request.POST['inputMobile']
        if 'inputImage' in request.FILES and len(request.FILES['inputImage']) > 0:
            trainer.image = request.FILES['inputImage']
        trainer.save()
        trainer = Trainer.objects.get(user=request.user)
    
    context = {
        'title': "Edit profile", 
        'trainer': trainer 
    }
    return render(request,'userprofile_edit.html',context )

@login_required(login_url='/')
def change_password_view(request):
    user = request.user   
    trainer = Trainer.objects.get(user=user)
    
    context = {
        'title': "Edit profile", 
        'trainer': trainer 
    }
    old_password = request.POST['inputOldPassword']
    is_password_correct = check_password(old_password, user.password)
    if is_password_correct:
        password1 = request.POST['inputNewPassword']
        password2 = request.POST['inputRepeatPassword']
        if password1 == password2:         
            user.set_password(password1)
            user.save()
            messages.error(request, 'The password has been changed!', extra_tags='alert-success')
        else:
            messages.error(request, 'The passwords is not correct!', extra_tags='alert-danger')
    else:
        messages.error(request, 'The passwords is not correct!', extra_tags='alert-danger')

    return render(request,'userprofile_edit.html',context )

@login_required(login_url='/')
def players_trainer_view(request):
    trainer = Trainer.objects.get(user=request.user)

    players = Player.objects.filter(trainer=trainer)
    context = {
        'title': "Players", 
        'trainer': trainer, 
        'players': players
    }
    return render(request,'playersTrainer.html',context )

@login_required(login_url='/')
def add_player_view(request):
    trainer = Trainer.objects.get(user=request.user)
    fees = MembershipFeeType.objects.all()
    context = {
        'title': "Add player", 
        'trainer': trainer,
        'fees': fees 
    }
    return render(request,'addPlayer.html',context )

@login_required(login_url='/')
def edit_player_view(request,player_id):
    trainer = Trainer.objects.get(user=request.user)
    player = Player.objects.get(id=player_id)
    fees = MembershipFeeType.objects.all()
    context = {
        'title': "Edit player", 
        'trainer': trainer,
        'fees': fees, 
        'player': player
    }
    return render(request,'editPlayer.html',context )

@login_required(login_url='/')
def save_player_view(request):
    
    trainer = Trainer.objects.get(user=request.user)
    first_name = request.POST['inputFirstName']
    last_name = request.POST['inputLastName']
    username = generate_username(first_name=first_name, last_name=last_name)
    email= request.POST['inputEmail']
    oib = request.POST['inputOIB']
    player_exists = Player.objects.filter(oib=oib).exists()
    if player_exists:
        messages.error(request, 'Ovaj OIB već postoji. Pronađite igrača u sustavu za pretraživanje.', extra_tags='alert-danger')
        fees = MembershipFeeType.objects.all()
        context = {
        'title': "Add player", 
        'trainer': trainer,
        'fees': fees 
         }
        return render(request,'addPlayer.html',context )
   
     
    user = User.objects.create(
        username=username,
        password=generate_random_password(),
        email=email
    )
    user.first_name=first_name
    user.last_name= last_name
    user.save()
    
    try:
        birthday = datetime.strptime(request.POST['inputBirthday'], '%Y-%m-%d').date()
    except ValueError:
        pass
   
    player = Player.objects.create(
         user=user,
         birthday=birthday   
         )
    player.trainer=trainer
    player.oib = oib
    selected_fee_id = request.POST.get('fee')
    try:
        selected_fee = MembershipFeeType.objects.get(id=selected_fee_id)
        player.membership_fee_type=selected_fee
    except MembershipFeeType.DoesNotExist:
        pass
    
    
    player.father_name = request.POST['inputFathersName']
    player.mobile = request.POST['inputMobile']
    if 'inputImage' in request.FILES and len(request.FILES['inputImage']) > 0:
            player.image = request.FILES['inputImage']
    if 'inputAccessCard' in request.FILES and len(request.FILES['inputAccessCard']) > 0:
            player.access_card = request.FILES['inputAccessCard']
    if 'inputCertificate' in request.FILES and len(request.FILES['inputCertificate']) > 0:
            player.cartificate_of_nationality = request.FILES['inputCertificate']
    
    try:
        player.medical_examination = datetime.strptime(request.POST['inputMedical'], '%Y-%m-%d').date()
    except ValueError:
        pass
     
    player.save()
    players = Player.objects.filter(trainer=trainer)
    context = {
        'title': "Players", 
        'trainer': trainer, 
        'players': players
    }

    return render(request,'playersTrainer.html',context )

@login_required(login_url='/')
def save_edit_player_view(request, player_id):

    trainer = Trainer.objects.get(user=request.user)
    player = Player.objects.get(id=player_id)
    first_name = request.POST['inputFirstName']
    last_name = request.POST['inputLastName']
    email= request.POST['inputEmail']

    oib = request.POST['inputOIB']
    player_exists = Player.objects.filter(oib=oib).exists()
    
    if player_exists and player.oib != oib:
        messages.error(request, 'Ovaj OIB već postoji. Pronađite igrača u sustavu za pretraživanje.', extra_tags='alert-danger')
        fees = MembershipFeeType.objects.all()
        context = {
        'title': "Edit player", 
        'trainer': trainer,
        'fees': fees, 
        'player': player
        }
        return render(request,'editPlayer.html',context )
    
    
     
    player.user.first_name=first_name
    player.user.last_name= last_name
    player.user.email = email
    player.user.save()
    
    try:
        player.birthday = datetime.strptime(request.POST['inputBirthday'], '%Y-%m-%d').date()
    except ValueError:
        pass
   
    selected_fee_id = request.POST.get('fee')
    try:
        selected_fee = MembershipFeeType.objects.get(id=selected_fee_id)
        player.membership_fee_type=selected_fee
    except MembershipFeeType.DoesNotExist:
        pass

    player.oib = oib
    player.father_name = request.POST['inputFathersName']
    player.mobile = request.POST['inputMobile']
    if 'inputImage' in request.FILES and len(request.FILES['inputImage']) > 0:
            player.image = request.FILES['inputImage']
    if 'inputAccessCard' in request.FILES and len(request.FILES['inputAccessCard']) > 0:
            player.access_card = request.FILES['inputAccessCard']
    if 'inputCertificate' in request.FILES and len(request.FILES['inputCertificate']) > 0:
            player.cartificate_of_nationality = request.FILES['inputCertificate']
    
    try:
        player.medical_examination = datetime.strptime(request.POST['inputMedical'], '%Y-%m-%d').date()
    except ValueError:
        pass
     
    player.save()
    players = Player.objects.filter(trainer=trainer)
    context = {
        'title': "Players", 
        'trainer': trainer, 
        'players': players
    }
    return render(request,'playersTrainer.html',context )

@login_required(login_url='/')
def add_player_on_list_view(request, player_id):

    trainer = Trainer.objects.get(user=request.user)
    player = Player.objects.get(id=player_id)
    player.trainer = trainer
    player.save()
    players = Player.objects.filter(trainer=trainer)
    context = {
        'title': "Players", 
        'trainer': trainer, 
        'players': players
    }
    return render(request,'playersTrainer.html',context )

@login_required(login_url='/')
def remove_player(request, player_id):
    trainer = Trainer.objects.get(user=request.user)
    player = Player.objects.get(id=player_id)
    player.trainer = None
    player.save()
    players = Player.objects.filter(trainer=trainer)
    context = {
        'title': "Players", 
        'trainer': trainer, 
        'players': players
    }
    return render(request,'playersTrainer.html',context )

@login_required(login_url='/')
def search_player_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('query', '')
        if len(query) >= 3:
            courent_trainer = Trainer.objects.get(user=request.user)
            players = Player.objects.filter(Q(trainer=None) | ~Q(trainer = courent_trainer) ,Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))[:10]
            
            results =[]
            for player in players:
                add_player_url = reverse('addplayeronlist', kwargs={'player_id': player.id})
                player_data = {
                    'id': player.id,
                    'first_name': player.user.first_name,
                    'last_name': player.user.last_name,
                    'add_player_url': add_player_url
                }
                if player.image:  # Provjera postojanja image-a
                    player_data['image'] = player.image.url
                else:
                    player_data['image'] = ''
                results.append(player_data)
            return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url='/')
def trainings_view(request):
    trainer = Trainer.objects.get(user=request.user)
    trainings = Training.objects.filter(trainer=trainer).order_by('-date')
    context = {
        'title': "Trainings", 
        'trainer': trainer,
        'trainings':trainings, 
    }
    return render(request,'trainings.html',context )


@login_required(login_url='/')
def add_replacemant_training_view(request, trainer_id):
    trainer = Trainer.objects.get(user=request.user)
    if trainer_id==trainer:
        players = Player.objects.filter(trainer=trainer)
        avPlayers = Player.objects.filter( ~Q(trainer = trainer))
    else:
        players = Player.objects.filter(trainer=trainer_id)
        avPlayers = Player.objects.filter( ~Q(trainer = trainer_id))
   
    trainers = Trainer.objects.filter( ~Q(id = trainer.id))  
    replacement = Trainer.objects.get(id=trainer_id)
    
    context = {
        'title': "Add Training", 
        'trainer': trainer, 
        'training_durations':Training.TRANING_DURATIONS,
        'current_date':date.today(),
        'players':players,
        'trainers':trainers,
        'available_players':avPlayers,
        'add_replacement_url': reverse('addreplacemanttraining', args=[trainer_id]),
        'replace': replacement
    }
    return render(request,'addReplacemantTraining.html',context )

@login_required(login_url='/')
def save_training_view(request):
    trainer = Trainer.objects.get(user=request.user)
    try:
        date = datetime.strptime(request.POST['inputDate'], '%Y-%m-%d').date()
    except ValueError:
        pass
    training_duration = request.POST.get('duration')
   
    training = Training.objects.create(
        trainer = trainer,
        date = date,
        training_duration=training_duration
      
    )
    replacement_id = request.POST.get('replacemant')
    replacement = None
    if replacement_id and replacement_id!=str(trainer.id):
        replacement = Trainer.objects.get(id=replacement_id)
        training.replacement=replacement
    training.save()

    if replacement:
        players = Player.objects.filter(trainer=replacement)
    else:
        players = Player.objects.filter(trainer=trainer)

    for player in players:
        presence = True if request.POST.get(f'presence_{player.id}') == 'on' else False
        training_has_player = TrainingHasPlayers.objects.create(
            player = player,
            training = training,
            presence = presence
        )
        training_has_player.save()
    
    
    new_players_ids = request.POST.getlist('new_player')
    if new_players_ids:
        while '-1' in new_players_ids:
            new_players_ids.remove('-1')

        new_players_ids = list(dict.fromkeys(new_players_ids))
        
        for id in new_players_ids:
                player = Player.objects.get(id=id)
                training_has_new_player = TrainingHasPlayers.objects.create(
                player = player,
                training = training,
                presence = True
                )
                training_has_new_player.save()
       
    
    context = {
        'title': "Trainings", 
        'trainer': trainer, 
    }
    return redirect('trainings')

@login_required(login_url='/')
def save_edit_training_view(request,training_id):
    trainer = Trainer.objects.get(user=request.user)
    training = Training.objects.get(id=training_id)
    training_has_players = TrainingHasPlayers.objects.filter(training=training)
    try:
        date = datetime.strptime(request.POST.get('inputDate', ''), '%Y-%m-%d').date()
        training.date=date
    except ValueError:
        pass

    training.training_duration = request.POST.get('duration')
    
    training.save()

    for training_has_player in training_has_players:
        presence = True if request.POST.get(f'presence_{training_has_player.player.id}') == 'on' else False
        training_has_player.presence=presence
        training_has_player.save()
    
    new_players_ids = request.POST.getlist('new_player')
    if new_players_ids:
        while '-1' in new_players_ids:
            new_players_ids.remove('-1')

        new_players_ids = list(dict.fromkeys(new_players_ids))
        
        for id in new_players_ids:
                player = Player.objects.get(id=id)
                try:
                    training_has_new_player = TrainingHasPlayers.objects.create(
                    player = player,
                    training = training,
                    presence = True
                    )
                    training_has_new_player.save()
                except IntegrityError:
                    messages.error(request, 'Igrač kojeg ste dodali već postoji u listi!', extra_tags='alert-danger')
                    return redirect('edittraining',training_id)
    context = {
        'title': "Trainings", 
        'trainer': trainer, 
    }
    return redirect('trainings')

@login_required(login_url='/')
def edit_training_view(request,training_id):
    trainer = Trainer.objects.get(user=request.user)
    training = Training.objects.get(id=training_id)
    presences = TrainingHasPlayers.objects.filter(training=training)
    fees = MembershipFeeType.objects.all()
    if training.replacement:
        avPlayers = Player.objects.filter( ~Q(trainer = training.replacement))
    else:
        avPlayers = Player.objects.filter( ~Q(trainer = trainer))
    context = {
        'title': "Edit training", 
        'trainer': trainer,
        'fees': fees, 
        'training': training,
        'training_durations':Training.TRANING_DURATIONS,
        'presences':presences,
        'available_players':avPlayers,
    }
    return render(request,'editTraining.html',context )

@login_required(login_url='/')
def delete_training_view(request, training_id):
    training = Training.objects.get(id=training_id)
    training.delete()
    return redirect('trainings')
 

def generate_username(first_name, last_name):
    # Kombiniraj ime i prezime
    full_name = f"{first_name}{last_name}".lower()
    
    clean_name = re.sub(r'[šćčđž]', lambda m: {'š': 's', 'ć': 'c', 'č': 'c', 'đ': 'd', 'ž': 'z'}.get(m.group(0)), full_name)
   
    clean_name = re.sub(r'\W+', '', clean_name)
    
    # Ako je ime i prezime prazno nakon uklanjanja posebnih znakova,
    # generiraj generičko korisničko ime
    if not clean_name:
        clean_name = 'user'
    
    # Provjeri postoji li već korisnik s generiranim korisničkim imenom
    suffix = ''
    username = clean_name
    counter = 1
    while User.objects.filter(username=username).exists():
        suffix = str(counter)
        username = f"{clean_name}{suffix}"
        counter += 1
    
    return username

def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(10))
    return make_password(password)