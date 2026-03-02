from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserLoginForm, ChangePasswordForm
from portfolio.models import PortfolioEntry, PortfolioCategory, PortfolioVideo
from main.models import ContactMessage


# S'enregistrer
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# Login
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:admin_index')
            else:
                print("Authentication failed: user is None")
        else:
            print("Form is not valid")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# Logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('main:index')


# Account detail
@login_required
def my_account(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'accounts/my_account.html', context)


### ADMIN ###
# Admin redirect
@login_required
def admin_redirect(request):
    return redirect('accounts:admin_index')


# Admin redirect
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_index(request):
    context = {
        'admin_section': 'dashboard',
        'stats': {
            'total_entries':     PortfolioEntry.objects.count(),
            'published_entries': PortfolioEntry.objects.filter(is_published=True).count(),
            'total_categories':  PortfolioCategory.objects.count(),
            'total_videos':      PortfolioVideo.objects.count(),
            'unread_messages':   ContactMessage.objects.filter(is_read=False).count(),
        },
        'recent_entries':  PortfolioEntry.objects.select_related('category').order_by('-created_at')[:5],
        'unread_messages':  ContactMessage.objects.filter(is_read=False).count(),
        'recent_messages':  ContactMessage.objects.order_by('-created_at')[:4],
    }
    return render(request, 'accounts/admin/index.html', context)


# Messages de contact
@login_required
@user_passes_test(lambda u: u.is_superuser)
def contact_messages(request):
    msgs = ContactMessage.objects.all()
    return render(request, 'accounts/admin/contact_messages.html', {
        'contact_messages': msgs,
        'admin_section':    'contact',
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def contact_message_detail(request, pk):
    from django.shortcuts import get_object_or_404
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save()
    return render(request, 'accounts/admin/contact_message_detail.html', {
        'msg':           msg,
        'admin_section': 'contact',
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def contact_message_delete(request, pk):
    from django.shortcuts import get_object_or_404
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message supprimé.')
        return redirect('accounts:contact_messages')
    return render(request, 'accounts/admin/contact_message_detail.html', {
        'msg':           msg,
        'confirm_delete': True,
        'admin_section': 'contact',
    })


# Change password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                if form.cleaned_data['new_password'] == form.cleaned_data['confirm_password']:
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Votre mot de passe a été changé avec succès.')
                    if not user.is_superuser:
                        return redirect(reverse_lazy('accounts:my_account'))
                    else:
                        return redirect(reverse_lazy('accounts:admin_index'))
                else:
                    messages.error(request, 'Les nouveaux mots de passe ne correspondent pas.')
            else:
                messages.error(request, 'L\'ancien mot de passe est incorrect.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = ChangePasswordForm()
    return render(request, 'accounts/password_reset/change_password.html', {'form': form})