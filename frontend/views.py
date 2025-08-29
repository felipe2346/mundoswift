from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string


from account.models import Shipment, LiveUpdate
from . import emailsend

def home(request):
    return render(request, 'frontend/index.html')


def about(request):
    return render(request, 'frontend/about_us.html')


def service(request):
    return render(request, 'frontend/service.html')


def tracking(request):
    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code')
        shipments = Shipment.objects.filter(tracking_number=tracking_code)

        if shipments.exists():
            shipment_single = shipments.first()
            live_update_qs = LiveUpdate.objects.filter(shipment=shipment_single).order_by('created_on')

            # Serialize live updates to a list of dicts for the map
            live_updates = []
            for update in live_update_qs:
                if update.latitude and update.longitude:
                    live_updates.append({
                        'latitude': update.latitude,
                        'longitude': update.longitude,
                        'status': update.status,
                        'remark': update.remark,
                        'created_on': update.created_on.isoformat(),
                        'country': update.country.country_name if update.country else None,
                    })

            live_update_count = live_update_qs.count()
            latest_update = live_update_qs.last()

            return render(request, 'frontend/tracking.html', {
                'shipments': shipments,
                'shipment_single': shipment_single,
                'update_count': live_update_count,
                'latest_update': latest_update,
                'live_update': live_update_qs,
                'live_updates_json': live_updates,  # Pass serialized updates for JS
            })
        else:
            messages.error(request, "Invalid tracking code. Please check the code and try again.")
            return redirect('frontend:tracking')

    return render(request, 'frontend/tracking.html')


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account:dashboard')    
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'frontend/login.html')


@login_required()
def logoutUser(request):
	logout(request)
	return redirect('frontend:login')



def contact_us(request):

    if request.method == 'POST':
        print('button clicked')
        name = request.POST.get('contact-name')
        email = request.POST.get('contact-email')
        subject = request.POST.get('contact-subject')
        message = request.POST.get('contact-message')

        final_message = render_to_string('frontend/emails/customer_care_email.html', 
        {
            'name': name,
            'email': email,
            'message': message,
            'subject': subject
        })

        try:
            emailsend.email_send(
                'Email From '+name,
                final_message,
                'deliveries@mundoswift.com',
            )
            messages.success(request, 'Email sent successfully, we will get back to you as soon as possible')
        except:
            messages.error(request, 'There was an error while trying to send your email, please try again')

        finally:
            return redirect('frontend:contact_us')
    return render(request, 'frontend/contact.html')
