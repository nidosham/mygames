
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import *
from django.contrib.sessions.models import Session
from mygames.models import *
import datetime
from django.views import generic
from django.views.decorators.clickjacking import xframe_options_exempt
from hashlib import md5
from .models import Post
from django.utils import timezone
from django.template import RequestContext

# logged_users = LoggedUser.objects.all().order_by('username')
# logged_users = [user.user for user in LoggedUser.objects.all()]

the_username = ""


def logged(request):
    logged_users = LoggedUser.objects.all().order_by('username')
    return render('users/logged.html',
                  {'logged_users': logged_users},
                  context_instance=RequestContext(request))


# logged_users = [user.user for user in LoggedUser.objects.all()]

'''ef messages(request, postid):
    posts = post(id=postid)
    messa(request, postid):
    posts = post(id=postid)
    messageList = Message.objects.all(post=post)
    return render(request, 'mygames/messages.html', {'messageList': messageList})
'''


def login_user(sender, request, user, **kwargs):
    LoggedUser(username=user.username).save()


def logout_user(sender, request, user, **kwargs):
    try:
        if user:
            u = LoggedUser.objects.get(pk=user.username)
            u.delete()
    except LoggedUser.DoesNotExist:
        pass


user_logged_in.connect(login_user)
user_logged_out.connect(logout_user)


def mymessages(request):
    user = User.objects.get(username="admin")
    posts = Post.objects.filter(author=user)
    messageList = []
    for p in posts:
        if Message.objects.filter(post=p).values():
            print("hahahaha ", Message.objects.filter(post=p).values())
            messageList.extend(Message.objects.filter(post=p))
    return render(request, 'mygames/messages.html', {'messageList': messageList})


def faqs(request):
    return render(request, 'mygames/faqs.html')


def myinbox(request, id):
    message = Message.objects.get(id=id)
    return render(request, 'mygames/mymessage.html', {'message': message})


def about(request):
    return render(request, 'mygames/aboutus.html')


def profile(request):
    user = User.objects.get(username=the_username)
    gameList = CustomUser.objects.all()
    postList = Post.objects.filter(author=user)
    return render(request, "mygames/profile.html", {'postList': postList, 'gameList': gameList,  'name': the_username})


def home(request):
    gameList = Games.objects.all()
    postList = Post.objects.all()

    return render(request, 'mygames/home.html', {'postList': postList, 'gameList': gameList,  'name': the_username})


@xframe_options_exempt
def index(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # process data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            global the_username
            the_username = username
            if user is not None:
                # request.session.create()
                return HttpResponseRedirect(reverse('home'))

            else:
                # if (request.session.session_key == None):
                return HttpResponse("user is not authenticated")
        else:
            return HttpResponse("form is not valid")
    form = LoginForm()
    return render(request, 'mygames/login.html', {'form': form})


def settings(request):
    if request.method == 'POST':
        form = settingForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["can_Search"]
            message = form.cleaned_data["can_Message"]
            if delete:
                User.objects.get(user=user)
            return render(request, 'mygames/settings.html', {'form': form})
    form = settingForm()
    return render(request, 'mygames/settings.html', {'form': form})


def gameDetail(request, id):
    game = Games.objects.get(id=id)
    postList = Post.objects.filter(game=game)
    return render(request, 'mygames/theGame.html', {'game': game, 'postList': postList})


def postDetail(request, id=id):
    if request.method == "POST":
        form = messageForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            content = form.cleaned_data['message']
            post = Post.objects.get(id=id)
            user = User.objects.get(username=username)
            cuser = CustomUser.objects.get(player=user)
            message = Message(contact=cuser, post=post,
                              email=email, content=content)
            print("username:", username, "email:", email)
            message.save()
    print("Escape yyyyy")
    form = messageForm()
    post = Post.objects.get(id=id)
    return render(request, 'mygames/thepost.html', {'post': post, 'form': form, 'uname': the_username})


def getGameName(gameQuery):
    st1 = gameQuery.__str__()
    k = len(st1)-3
    game_name = st1[19:k]
    return game_name


def getUsName(q):
    st1 = q.__str__()
    k = len(st1)-3
    uname = st1[19:k]
    return uname


@ xframe_options_exempt
def registration(request):
    global the_username
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirmPassword = form.cleaned_data['confirmPassword']
            email = form.cleaned_data['email']
            gamesplayed = form.cleaned_data['games']
            favourite = form.cleaned_data['favourite']

            user = User.objects.create_user(username, email, password)
            fav = getGameName(favourite)
            played = getGameName(gamesplayed)
            favg = Games.objects.get(name=fav)
            playedg = Games.objects.get(name=played)

            c = CustomUser(player=user, favourite=fav)
            c.save()
            gp = GamesPlayed(player=c, game=playedg)
            gp.save()
            return render(request, 'mygames/registration.html', {'form': form, 'flag': True})

    form = RegistrationForm()
    return render(request, 'mygames/registration.html', {'form': form})


def addgame(request):
    '''session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    admin = CustomUser.objects.get(user=user)'''
    form = AddGameForm(request.POST)
    if request.method == "POST":

        if form.is_valid():  # if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            url = form.cleaned_data['url']
            imagepath = form.cleaned_data['imagepath']
            description = form.cleaned_data['description']
            game = Games(name=name, category=category, price=price, url=url,
                         admin=admin, image_path=imagepath, description=description)
            game.save()
            return render(request, 'mygames/addgame.html', {'form': form, 'flag': True})
    else:
        return render(request, 'mygames/addgame.html', {'form': form, 'formFlag': False})

    form = AddGameForm()
    return render(request, 'mygames/addgame.html', {'form': form})


def createpost(request):
    user = User.objects.get(username=the_username)
    player = CustomUser.objects.get(player=user)

    if request.method == "POST":
        form = postForm(request.POST)
        if form.is_valid():
            author = user
            game = form.cleaned_data['game']
            title = form.cleaned_data['title']
            descript = form.cleaned_data['description']
            playerno = dict(form.fields['playerno'].choices)[
                int(form.cleaned_data['playerno'])]
            request_duration = dict(
                form.fields['request_duration'].choices)[int(form.cleaned_data['request_duration'])]
            joinstatus = form.cleaned_data['request_status']
            messagestatus = form.cleaned_data['message_status']

            st1 = game.__str__()
            k = len(st1)-3
            game_name = st1[19:k]
            g = Games.objects.get(name=game_name)

            post = Post(author=user, title=title, description=descript, playerno=playerno,
                        request_duration=request_duration, requestStatus=joinstatus, messageStatus=messagestatus,
                        game=g)
            post.save()

            return render(request, 'mygames/createpost.html', {'form': form, 'flag': True})

    form = postForm()
    return render(request, 'mygames/createpost.html', {'form': form})


def editpost(request, id):
    user = User.objects.get(username=the_username)
    player = CustomUser.objects.get(player=user)

    if request.method == "POST":
        form = postForm(request.POST)
        if form.is_valid():
            author = user
            game = form.cleaned_data['game']
            title = form.cleaned_data['title']
            descript = form.cleaned_data['description']
            playerno = dict(form.fields['playerno'].choices)[
                int(form.cleaned_data['playerno'])]
            request_duration = dict(
                form.fields['request_duration'].choices)[int(form.cleaned_data['request_duration'])]
            joinstatus = form.cleaned_data['request_status']
            messagestatus = form.cleaned_data['message_status']

            st1 = game.__str__()
            k = len(st1)-3
            # get name of the game from returned querystring
            game_name = st1[19:k]
            g = Games.objects.get(name=game_name)

            post = Post(author=user, title=title, description=descript, playerno=playerno,
                        request_duration=request_duration, requestStatus=joinstatus, messageStatus=messagestatus,
                        game=g)
            post.save()

            return render(request, 'mygames/createpost.html', {'form': form, 'flag': True})


def mygames(request):
    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    player = CustomUser.objects.get(user=user)
    boughtGames = PurchasedGame.objects.filter(player=player)
    return render(request, 'authtest/home.html', {'boughtGames': boughtGames, 'user': user})


def deletegame(request, game_id):
    game = Games.objects.get(pk=game_id)
    game.delete()
    return HttpResponseRedirect(reverse('adminhome'))


def editgame(request, game_id):
    game = Games.objects.get(pk=game_id)
    if request.method == "POST":
        game.name = request.POST.get('name')
        game.category = request.POST.get('category')
        game.url = request.POST.get('url')
        game.image_path = request.POST.get('imagepath')
        game.description = request.POST.get('description')
        game.save()
        return render(request, 'mygames/editgame.html', {'flag': True})
    return render(request, 'mygames/editgame.html', {'game': game})


def allgames(request):
    games = Games.objects.all()
    return render(request, 'mygames/allgames.html', {'games': games})


@ xframe_options_exempt
def adminhome(request):
    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    admin = CustomUser.objects.get(user=user)
    games = Games.objects.filter(admin=admin)
    return render(request, 'mygames/adminhome.html', {'games': games})


@ xframe_options_exempt
def playerhome(request):
    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    player = CustomUser.objects.get(user=user)
    games = Games.objects.all()
    deleted = []
    if request.method == "POST":
        pid = request.POST.get('pid')
        sid = request.POST.get('sid')
        amount = request.POST.get('amount')
        secret_key = request.POST.get('token')
        checksumstr = "pid={}&sid={}&amount={}&token={}".format(
            pid, sid, amount, secret_key)
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()
        return JsonResponse({'checksum': checksum})
    return render(request, 'mygames/playerhometest.html', {'games': games, 'user': user})


def searchresults(request):
    games = Games.objects.all()
    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    player = CustomUser.objects.get(user=user)
    if request.method == "POST":
        search = request.POST.get('search')
        cat = request.POST.get('cat')
        if cat == 'all':
            games = Games.objects.filter(name__contains=search)
            for g in games:
                if PurchasedGame.objects.filter(game=g, player=player).exists():
                    games = games.exclude(id=g.id)
            return render(request, 'mygames/searchresults.html', {'games': games})
        else:
            games = Games.objects.filter(name__contains=search, category=cat)
            for g in games:
                if PurchasedGame.objects.filter(game=g, player=player).exists():
                    games = games.exclude(id=g.id)
    return render(request, 'mygames/searchresults.html', {'games': games})


@ xframe_options_exempt
def mygames(request):
    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    player = CustomUser.objects.get(user=user)
    return render(request, 'mygames/mygamestest.html', {'user': user})


def contactus(request):
    return render(request, 'mygames/contactus.html')


def myposts(request):
    user = User.objects.get(username=the_username)
    print("HHHHHHHH ", user.username)
    posts = Post.objects.filter(author=user)

    return render(request, 'mygames/myposts.html', {'postList': posts})


def logout(request):
    # logout(request)
    return HttpResponseRedirect(reverse('index'))


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
