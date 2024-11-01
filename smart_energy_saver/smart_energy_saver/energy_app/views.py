from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use get() instead of direct access
        password = request.POST.get('password')
        print("Received password:", password)  # Debug print statement

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def dashboard_view(request):
    energy_data = EnergyConsumption.objects.filter(user=request.user)
    carbon_data = CarbonFootprint.objects.filter(user=request.user).last()
    return render(request, 'dashboard.html', {
        'energy_data': energy_data,
        'carbon_data': carbon_data
    })
@login_required
def energy_tips_view(request):
    tips = EnergyTip.objects.all()
    return render(request, 'energy_tips.html', {'tips': tips})

@login_required
def energy_visualization_view(request):
    energy_data = EnergyConsumption.objects.filter(user=request.user)
    dates = [data.date for data in energy_data]
    usage = [data.energy_used for data in energy_data]

    # Plotting the data
    plt.figure(figsize=(10, 5))
    plt.plot(dates, usage, marker='o')
    plt.title('Energy Consumption Over Time')
    plt.xlabel('Date')
    plt.ylabel('Energy (kWh)')
    plt.grid(True)

    # Save the plot to a string buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'energy_visualization.html', {'graph': graph})

@login_required
def carbon_calculator_view(request):
    if request.method == 'POST':
        energy_used = float(request.POST['energy_used'])
        carbon_saved = energy_used * 0.707  # Example conversion factor
        CarbonFootprint.objects.create(user=request.user, carbon_saved=carbon_saved)
        return redirect('dashboard')
    return render(request, 'carbon_calculator.html')

def community_view(request):
    return render(request, 'community.html')
