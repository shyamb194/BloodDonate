from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.mail import EmailMessage


from .models import *
from .forms import *
from .tokens import account_activation_token

# Create your views here.
def activateAccount(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('UserAuthentication_app:login')
    else:
    	messages.success(request, 'The account for this link is already activated!')
    	return redirect('UserAuthentication_app:login')


def sendMail(request, user):
	user = User.objects.get(username = user)
	mail_subject = 'Activate your account.'
	message = render_to_string('UserAuthentication/acc_active_email.html', {
		'user': user,
		'domain': get_current_site(request).domain,
		'uid':urlsafe_base64_encode(force_bytes(user.pk)),
		'token':account_activation_token.make_token(user),
		})
	to_email = user.email
	email = EmailMessage(mail_subject, message, 'shyamb194@gmail.com', [to_email])
	email.content_subtype = "html"
	email.send(fail_silently=False)
	return redirect('UserAuthentication_app:login')

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('profile_app:profileTimeline')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		try:
			emailuser = User.objects.get(Q(email = username) | Q(username = username))
			if emailuser.is_active:
				user = authenticate(request, username = username, password = password)
				if user is not None:
					login(request, user)
					print(emailuser.username)
					return redirect('profile_app:profileTimeline', username = emailuser.username)
			else:
				messages.success(request, 'Please Confirm your email account before you can login', extra_tags='emaillogin')
				return render(request, 'UserAuthentication/login.html', {'emailuser': emailuser})
		except:
			try:
				mobileuser = ProfileDetails.objects.select_related('user').get(contact = username)
				print(mobileuser.user.is_active)
				if mobileuser.user.is_active:
					print('2')
					user = authenticate(request, username = username, password = password)
					print('3')
					if user is not None:
						login(request, user)
						return redirect('profile_app:profileTimeline', username = mobileuser.user.username)
				else:
					messages.success(request, 'Please Confirm your email account before you can login', extra_tags='mobilelogin')
					return render(request, 'UserAuthentication/login.html', {'mobileuser': mobileuser})
			except:
				messages.success(request, 'Username or password is incorrect')
			

	context = {}
	return render(request, 'UserAuthentication/login.html', context)

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('profile_app:profileTimeline')
	else:
		createUserForm = CreateUserForm()
		profileDetailsForm = ProfileDetailsForm()
		if request.method == 'POST':
			createUserForm = CreateUserForm(request.POST)
			profileDetailsForm = ProfileDetailsForm(request.POST)
			if createUserForm.is_valid() and profileDetailsForm.is_valid():
				user = createUserForm.save(commit=False)
				user.is_active = False				
				user.save()
				if 'pvtNumCheck' in request.POST:
					ProfileDetails.objects.create(
							user = user,
							gender = profileDetailsForm.cleaned_data.get('gender'),
							bloodGroup = profileDetailsForm.cleaned_data.get('bloodGroup'),
							dob = profileDetailsForm.cleaned_data.get('dob'),
							contact = profileDetailsForm.cleaned_data.get('contact'),
							contact_audience = 'private',
							permCountry = profileDetailsForm.cleaned_data.get('permCountry'),
							permState = profileDetailsForm.cleaned_data.get('permState'),
							permDistrict = profileDetailsForm.cleaned_data.get('permDistrict'),
							permCity = profileDetailsForm.cleaned_data.get('permCity'),
							tempCountry = profileDetailsForm.cleaned_data.get('tempCountry'),
							tempState = profileDetailsForm.cleaned_data.get('tempState'),
							tempDistrict = profileDetailsForm.cleaned_data.get('tempDistrict'),
							tempCity = profileDetailsForm.cleaned_data.get('tempCity'),
						)
				else:
					ProfileDetails.objects.create(
							user = user,
							gender = profileDetailsForm.cleaned_data.get('gender'),
							bloodGroup = profileDetailsForm.cleaned_data.get('bloodGroup'),
							dob = profileDetailsForm.cleaned_data.get('dob'),
							contact = profileDetailsForm.cleaned_data.get('contact'),
							contact_audience = 'public',
							permCountry = profileDetailsForm.cleaned_data.get('permCountry'),
							permState = profileDetailsForm.cleaned_data.get('permState'),
							permDistrict = profileDetailsForm.cleaned_data.get('permDistrict'),
							permCity = profileDetailsForm.cleaned_data.get('permCity'),
							tempCountry = profileDetailsForm.cleaned_data.get('tempCountry'),
							tempState = profileDetailsForm.cleaned_data.get('tempState'),
							tempDistrict = profileDetailsForm.cleaned_data.get('tempDistrict'),
							tempCity = profileDetailsForm.cleaned_data.get('tempCity'),
						)
				sendMail(request, user)
				user = createUserForm.cleaned_data.get('username')
				messages.success(request, 'Account Successfully Created for ' + user + ' Please Confirm your email before you login.')
				return redirect('UserAuthentication_app:login')



		context = {
			'createUserForm': createUserForm,
			'profileDetailsForm': profileDetailsForm,
		}
		return render(request, 'UserAuthentication/register.html', context)

def logOutUSer(request):
	logout(request)
	return redirect('UserAuthentication_app:login')













