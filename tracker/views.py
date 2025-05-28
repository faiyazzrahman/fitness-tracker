from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile
from django.db.models import Count
from django.db import transaction

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    new_user = user_form.save(commit=False)
                    new_user.set_password(user_form.cleaned_data['password'])
                    new_user.save()

                    profile = profile_form.save(commit=False)
                    profile.user = new_user
                    profile.save()  # Uses correct DB via model's save()

                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error during registration: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'tracker/registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def profile(request):
    try:
        profile = Profile.find_profile(request.user)
        if not profile:
            raise Profile.DoesNotExist
    except Profile.DoesNotExist:
        profile = None
    except Exception as e:
        messages.error(request, f'Error loading profile: {str(e)}')
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                
                # Get the updated profile from the correct database
                updated_profile = Profile.find_profile(request.user)
                messages.success(request, 'Your profile was updated successfully!')
                return redirect('profile')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'tracker/profile_edit.html', {
        'form': form,
        'profile': profile
    })

@login_required
def settings_view(request):
    try:
        profile = Profile.find_profile(request.user)
        if not profile:
            raise Profile.DoesNotExist
    except Profile.DoesNotExist:
        profile = None
    except Exception as e:
        messages.error(request, f'Error loading profile: {str(e)}')
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, 'Your profile was updated successfully!')
                return redirect('settings')  # Stay on settings page after update
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'tracker/settings.html', {
        'form': form,
        'profile': profile
    })


@login_required
def filter_by_body_type(request):
    try:
        selected_type = request.GET.get('body_type')
        if selected_type:
            # Search across all databases
            profiles = []
            for db in ['thin', 'medium', 'fat']:
                profiles.extend(list(Profile.objects.using(db).filter(body_type=selected_type.lower())))
        else:
            # Get all profiles from all databases
            profiles = []
            for db in ['thin', 'medium', 'fat']:
                profiles.extend(list(Profile.objects.using(db).all()))

        return render(request, 'tracker/filter_by_body_type.html', {
            'profiles': profiles,
            'selected_type': selected_type,
        })
    except Exception as e:
        messages.error(request, f'Error filtering profiles: {str(e)}')
        return render(request, 'tracker/filter_by_body_type.html', {
            'profiles': [],
            'selected_type': None,
        })

@login_required
def body_type_report(request):
    try:
        # Aggregate counts from all databases
        report = []
        for db in ['thin', 'medium', 'fat']:
            db_counts = Profile.objects.using(db).values('body_type').annotate(count=Count('body_type'))
            for item in db_counts:
                report.append(item)

        # Combine counts for the same body types
        combined_report = {}
        for item in report:
            body_type = item['body_type']
            combined_report[body_type] = combined_report.get(body_type, 0) + item['count']

        return render(request, 'tracker/body_type_report.html', {
            'report': [{'body_type': k, 'count': v} for k, v in combined_report.items()]
        })
    except Exception as e:
        messages.error(request, f'Error generating report: {str(e)}')
        return render(request, 'tracker/body_type_report.html', {
            'report': []
        })