from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LinkForm
from .models import Link, ShortLink
from .forms import UserUpdateForm


def home(request):
    return render(request, 'shortener/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'shortener/register.html', {'form': form})


@login_required
def dashboard(request):
    links = Link.objects.filter(user=request.user)
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect('dashboard')
    else:
        form = LinkForm()
    return render(request, 'shortener/dashboard.html', {'form': form, 'links': links})


def redirect_short_code(request, code):
    link = get_object_or_404(ShortLink, short=code)
    return redirect(link.original)


@login_required
def update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        user = request.user
        user.username = username
        user.email = email
        user.save()
        messages.success(request, 'Профіль оновлено успішно!')
        return redirect('dashboard')

    return render(request, 'shortener/update_profile.html')


@login_required
def user_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        user = request.user
        user.username = username
        user.email = email
        user.save()
        messages.success(request, 'Дані успішно оновлено!')
        return redirect('user_profile')

    return render(request, 'shortener/user_profile.html')


def logout_view(request):
    logout(request)
    return render(request, 'shortener/logged_out.html')


@login_required
def create_link(request):
    new_link = None
    links = ShortLink.objects.filter(user=request.user)

    if request.method == 'POST':
        long_url = request.POST.get('long_url')
        custom_slug = request.POST.get('custom_slug')

        if len(long_url) > 250:
            messages.error(request, f'Перевірте, щоб це значення містило не більше 250 символів (зараз {len(long_url)}).')
        elif ShortLink.objects.filter(short=custom_slug).exists():
            messages.error(request, 'Посилання з таким коротким словом вже існує.')
        else:
            new_link = ShortLink.objects.create(
                original=long_url,
                short=custom_slug,
                user=request.user
            )
            messages.success(request, 'Посилання успішно створено!')

    return render(request, 'shortener/create_link.html', {
        'new_link': new_link,
        'links': links,
    })


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'shortener/profile.html', {'form': form})

