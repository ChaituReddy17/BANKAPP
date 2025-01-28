from django.shortcuts import render, redirect
from .models import User, Transaction
from .forms import SignupForm, LoginForm
from django.contrib import messages
import random
import uuid
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.account_number = ''.join(random.choices('0123456789', k=16))
            user.save()
            messages.success(request, "Signup successful! Please login.")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username, password=password)
                request.session['user_id'] = user.id
                messages.success(request, "Login successful!")
                return redirect('home')
            except User.DoesNotExist:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found. Please login again.")
        return redirect('login')

    return render(request, 'home.html', {
        'username': user.username,
        'account_number': user.account_number,
        'balance': user.balance,
    })

def transfer_money_view(request):
    if request.method == "POST":
        sender_id = request.session.get('user_id')
        recipient_username = request.POST.get('recipient_username')
        recipient_account = request.POST.get('recipient_account')
        amount = float(request.POST.get('amount'))

        try:
            sender = User.objects.get(id=sender_id)
            recipient = User.objects.get(username=recipient_username, account_number=recipient_account)
            if sender.balance >= amount:
                sender.balance -= amount
                recipient.balance += amount
                sender.save()
                recipient.save()

                Transaction.objects.create(sender=sender, recipient=recipient, amount=amount)
                messages.success(request, "Transaction successful!")
            else:
                messages.error(request, "Insufficient balance.")
        except User.DoesNotExist:
            messages.error(request, "Recipient not found.")

    return redirect('home')

def generate_transaction_id():
    return str(uuid.uuid4())

def generate_otp():
    return random.randint(1000, 9999)
import smtplib
from email.mime.text import MIMEText

def send_email(receiver_email, otp):
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"
    subject = "Your OTP for Money Transfer"
    body = f"Your OTP for the transaction is: {otp}. Please do not share this with anyone."
    message = MIMEText(body)
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("OTP sent successfully!")
    except Exception as e:
        print(f"Failed to send OTP. Error: {e}")
def verify_and_transfer(request,user_otp, generated_otp, transaction_id, sender_account, receiver_account, amount):
    if user_otp == generated_otp:
        print(f"Transaction {transaction_id} successful!")
        print(f"{amount} has been transferred from {sender_account} to {receiver_account}.")
        return True
    else:
        print("Invalid OTP. Transaction failed.")
        return False
    if user_otp == generated_otp:
        sender_id = request.session.get('user_id')
        recipient_username = request.POST.get('recipient_username')
        recipient_account = request.POST.get('recipient_account')
        amount = float(request.POST.get('amount'))
        print(f"Transaction {transaction_id} successful!")
        print(f"{amount} has been transferred from {sender_account} to {receiver_account}.")
        return True
    else:
        print("Invalid OTP. Transaction failed.")
        return False
    try:
        sender = User.objects.get(id=sender_account)
        recipient = User.objects.get(username=recipient_username, account_number=recipient_account)
        if sender.balance >= amount:
            sender.balance -= amount
            recipient.balance += amount
            sender.save()
            recipient.save()
            Transaction.objects.create(sender=sender, recipient=recipient, amount=amount)
            messages.success(request, "Transaction successful!")
        else:
            messages.error(request, "Insufficient balance.")
    except User.DoesNotExist:
            messages.error(request, "Recipient not found.")


otp_store = {}

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sender = data.get('sender')
        receiver = data.get('receiver')
        amount = data.get('amount')
        email = data.get('email')

        otp = random.randint(1000, 9999)

        otp_store['otp'] = otp
        otp_store['sender'] = sender
        otp_store['receiver'] = receiver
        otp_store['amount'] = amount

        try:
            send_mail(
                "Your OTP for Money Transfer",
                f"Your OTP is: {otp}",
                "chaitanyasanikommu123@gmail.com",
                [email],
                fail_silently=False,
            )
            return JsonResponse({"success": True, "message": "OTP sent successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

from django.shortcuts import redirect
from django.http import JsonResponse

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_otp = int(data.get('otp'))

        if user_otp == otp_store.get('otp'):
            sender_account = int(otp_store.get('sender'))
            receiver_account = int(otp_store.get('receiver'))
            amount = int(otp_store.get('amount'))

            try:
                sender = User.objects.get(account_number=sender_account)
                receiver = User.objects.get(account_number=receiver_account)

                if sender.balance >= amount:
                    sender.balance = sender.balance-amount
                    receiver.balance = receiver.balance+ amount
                    sender.save()
                    receiver.save()

                    Transaction.objects.create(
                        sender=sender,
                        recipient=receiver,
                        amount=amount
                    )

                    otp_store.clear()

                    return JsonResponse({"success": True, "redirect_url": "/home/"})
                else:
                    return JsonResponse({"success": False, "message": "Insufficient balance."})
            except User.DoesNotExist:
                return JsonResponse({"success": False, "message": "Invalid sender or receiver account."})
        else:
            return JsonResponse({"success": False, "message": "Invalid OTP."})
        
def trans(request):
    return render(request,"transfer.html")


def lend(request):
    return render(request,'lend.html')

def logout(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username, password=password)
                request.session['user_id'] = user.id
                messages.success(request, "Login successful!")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})