import random
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def login_view(request):

    if request.method == "POST":
        email = request.POST.get("email")

        otp = random.randint(100000, 999999)

        # Store in session
        request.session['email'] = email
        request.session['otp'] = str(otp)

        # Email content
        subject = "Your OTP Code"
        from_email = settings.EMAIL_HOST_USER
        to = [email]

        html_content = f"""
        <div style="text-align:center; font-family:Arial;">
            <h2>Login Verification</h2>
            <p>Your One-Time Password is:</p>
            <div style="
                font-size:40px;
                font-weight:bold;
                background:#f4f4f4;
                padding:20px;
                display:inline-block;
                border-radius:10px;
                letter-spacing:10px;
            ">
                {otp}
            </div>
            <p>This OTP is valid for 5 minutes.</p>
        </div>
        """

        email_message = EmailMultiAlternatives(subject, "", from_email, to)
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        return redirect('verify')

    return render(request, 'accounts/login.html')


def verify_otp(request):

    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")

        if entered_otp == stored_otp:
            request.session.pop('otp', None)  # Clear OTP after success
            return render(request, 'accounts/dashboard.html')
        else:
            return render(request, 'accounts/verify.html', {
                "error": "Invalid OTP"
            })

    return render(request, 'accounts/verify.html')