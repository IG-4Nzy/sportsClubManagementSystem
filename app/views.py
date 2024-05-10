from . models import *
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.utils import timezone
from django.contrib.auth import logout
from django.core.mail import send_mail
from fuzzywuzzy import fuzz


# home 
def index(request):
    return render (request,'home/index.html')

# authentication 
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        user = auth.authenticate(username=email, password=password)
        print(user)
        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                return redirect('adminDash')
            elif UserProfile.objects.filter(user=user,role='club').exists():
                auth.login(request, user)
                user = UserProfile.objects.get(user=user)
                if(user.isProfileComplete == 'True' and user.isActive == 'True'):
                    return redirect('clubDash')
                else:
                    return redirect('clubProfileComplete')
            elif UserProfile.objects.filter(user=user,role='member').exists():
                auth.login(request, user)
                return redirect('memberDash')
            else:
                context = {'msg': 'User has no recognized role'}
        else:
            context = {'msg': 'Invalid email or password'}
    else:
        return render(request, 'auth/login.html')
    return render(request, 'auth/login.html', context)
def register(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastname = request.POST.get('surname')
        number = request.POST.get('number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        if User.objects.filter(username = email).exists():
            return render(request,'auth/register.html',{'msg':'user with this email  already exists'})
        user = User.objects.create_user(username=email,password=password,first_name = firstName,last_name=lastname)
        userProfile = UserProfile(
            user = user,
            number = number,
            dob = dob,
            gender = gender,
            role = role
        )
        userProfile.save()
        users = UserProfile.objects.get(user=user)
        if role =='club':
            club = Clubs(
                user=users
            )
            club.save()
            return redirect(login)
        else:
            members = Members(
                user=users
            ).save()
            return redirect(login)
    return render (request,'auth/register.html')
def logout_view(request):
    logout(request)
    return redirect(login)


# admin 
def adminDash(request):
    clubs = Clubs.objects.filter(user__role = 'club',user__isProfileComplete = "True")
    return render(request,'admin/adminDash.html',{'clubs':clubs})
def approve(request,id):
    user = UserProfile.objects.get(pk=id)
    user.isActive = 'True'
    send_mail(
            'A club registration request has been Approved',
            'you can log in now',
            'sampleproject2211@gmail.com',
            [user.user.email],
            fail_silently=False,
        )
    user.save()
    return redirect(adminDash)
def reject(request,id):
    user = UserProfile.objects.get(pk=id)
    user.isActive = 'False'
    send_mail(
        'A club registration request has been Rejected',
        'you can re apply when you are ready',
        'sampleproject2211@gmail.com',
        [user.user.email],
        fail_silently=False,
    )
    user.save()
    return redirect(adminDash)
def AdminviewMembers(request):
    return render(request,'admin/AdminviewMembers.html')


# club 
def clubDash(request):
    return render(request,'club/clubDash.html')
def clubProfileComplete(request):
    AdminUser = User.objects.get(is_superuser = True)
    user_profile = UserProfile.objects.get(user=request.user)
    club = Clubs.objects.get(user=user_profile)
    if request.method == 'POST':
        clubName = request.POST.get('club-name')
        description = request.POST.get('club-description')
        website = request.POST.get('club-website')
        license = request.POST.get('club-license')
        club.clubName = clubName
        club.description = description
        club.websites = website
        club.licence = license
        if 'club-image' in request.FILES:
            club.image = request.FILES['club-image']
        club.save() 
        user_profile.isProfileComplete = "True"
        send_mail(
            'A club has been registered',
            'Please verify the club',
            'sampleproject2211@gmail.com',
            [AdminUser.email],
            fail_silently=False,
        )
        user_profile.save()
        context = {'club': club}
        return render(request, 'club/clubProfileComplete.html', context)

    context = {'club': club}
    return render(request, 'club/clubProfileComplete.html', context)
def viewMembers(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    current_club = Clubs.objects.get(user=userprofile)
    club_members = Members.objects.filter(EnrolledSports__club=current_club)

    context = {
        'club_members': club_members
    }
    return render(request, 'club/viewMembers.html', context)
def addSports(request):
    userprofile = UserProfile.objects.get(user=request.user)
    club = Clubs.objects.get(user = userprofile)
    sports = Sports.objects.filter(club=club)
    context = {
        'sports':sports
    }
    if request.method=="POST":
        sportsName = request.POST.get('sport-name')
        description = request.POST.get('sport-description')
        img = request.POST.get('sport-image')
        fees = request.POST.get('sport-fees')
        sport = Sports.objects.create(
            name=sportsName,
            description=description,
            fees=fees,
            club=club,
            img = request.FILES['sport-image']
        )
        return redirect(addSports)
    return render(request,'club/addSports.html',context)
def removeSport(request,id):
    sports = Sports.objects.get(pk=id)
    sports.delete()
    return redirect(addSports)

# member 
def memberDash(request):
    user=request.user
    user = UserProfile.objects.get(user=user)
    enrolled_sports = Members.objects.filter(user=user)
    context = {
        'enrolled_sports':enrolled_sports
    }
    return render(request,'member/memberDash.html',context)
def cancel(request,id):
    user=request.user
    user = UserProfile.objects.get(user=user)
    enrolled_sports = Members.objects.get(pk=id)
    enrolled_sports.status = "Cancelled"
    enrolled_sports.dateOfQuit = timezone.now().date()
    enrolled_sports.save()
    context = {
        'enrolled_sports':enrolled_sports
    }
    return redirect(memberDash)
def enrollSports(request):
    if 'search_query' in request.GET:
        search_query = request.GET['search_query']
        all_sports = Sports.objects.all()
        matching_sports = []
        for sport in all_sports:
            match_ratio = fuzz.ratio(search_query.lower(), sport.name.lower())
            if match_ratio > 60:
                matching_sports.append(sport)
        context = {
            'sports': matching_sports,
            'search_query': search_query
        }
    else:
        sports = Sports.objects.all()
        context = {
            'sports': sports
        }
    return render(request, 'member/enrollSports.html', context)
def enroll(request,id):
    print(id)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    enrolled_sport = Sports.objects.get(pk=id) 
    print(enrolled_sport)
    date_of_enroll = timezone.now().date()
    print(date_of_enroll)
    Members.objects.create(user=user_profile, EnrolledSports=enrolled_sport, dateOfEnroll=date_of_enroll)
    return redirect('memberDash') 























