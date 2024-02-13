from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ProfileUpdateForm, UserRegistrationForm, UserUpdateForm
from votingapp.models import*
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout, authenticate

# Create your views here.
# this section is fuction as the registration function
def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    form=UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.username=user.username.lower()
            user.save()
            user_prof=Profile.objects.create(user=user)
            user_prof.save()
            login(request, user)
            return redirect("index")
    context={'form':form}
    return render(request, 'landing.html', context)

# this section handles the login view usin the fuction below 
def LoginView(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method =="POST":
        useremail=request.POST.get("Email")
        userpassword=request.POST.get("password")
        user=authenticate(request, username=useremail, password=userpassword)
        if user is not None:
            login(request, user)

            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("index")
        else:
            messages.error(request, "invalid credentials")
    return render(request, 'login.html')

# the section handles the logout view using the django inbuilt fuction called log
def logoutview(request):
    logout(request)
    return redirect("index")

# this fuction handles the profile of the user
def user_profile(request):
    return render(request, 'profile.html')

# this function handles updating the profile of the user  
def profile_update(request):
    try:
        # Attempt to retrieve the associated Profile instance
        profile_instance = request.user.profile
    except AttributeError:
        # If the profile attribute is not available, set profile_instance to None
        profile_instance = None

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()

            if not profile_instance:
                # If profile_instance is None, create a new Profile instance
                profile_instance = Profile(user=request.user)

            # Update the fields of the profile instance
            profile_instance.address = p_form.cleaned_data['address']
            profile_instance.phonenumber = p_form.cleaned_data['phonenumber']
            # Add other fields as needed

            profile_instance.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_instance)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, 'profile_update.html', context)