# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from user_APP.forms import SignInForm
from .models import Room, Booking
from .forms import RoomForm, BookingForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile_page')
    else:
        form = UserCreationForm()
    return render(request, 'prac_APP/register.html', {'form': form})

def login_view(request):  # функция входа на сайте
    if request.user.is_authenticated:
        return redirect('profile_page')
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)  # проверка пароля и логина
            if user is not None:  # проверка найден ли пользователь в бд
                login(request, user)
                return redirect('profile_page')
            else:
                print('User not found')
    form = SignInForm()
    ctx = {
        'form': form
    }
    return render(request, 'prac_APP/Login.html', ctx)


def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    return render(request, 'prac_APP/profile.html')

def room_list(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    rooms = Room.objects.all()
    return render(request, 'prac_APP/room_list.html', {'rooms': rooms})

def room_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('login_view')
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'prac_APP/room_detail.html', {'room': room})

def room_create(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    if request.method == "POST":
        form = RoomForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tadjiki')
    else:
        form = RoomForm()
    return render(request, 'prac_APP/room_create.html', {'form': form})


def room_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('login_view')
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'prac_APP/room_update.html', {'form': form})
def room_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('login_view')
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        room.delete()
        return redirect('room_list')
    return render(request, 'prac_APP/room_delete.html', {'room': room})

def booking_list(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'prac_APP/booking_list.html', {'bookings': bookings})

def booking_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('login_view')
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'prac_APP/booking_detail.html', {'booking': booking})

def booking_create(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'prac_APP/booking_form.html', {'form': form})

def booking_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('login_view')
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_detail', pk=pk)
    else:
        form = BookingForm(instance=booking)
    return render(request, 'prac_APP/booking_form.html', {'form': form})

def booking_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('login_view')
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        booking.delete()
        return redirect('booking_list')
    return render(request, 'prac_APP/booking_delete.html', {'booking': booking})


def logout_view(request):
    logout(request)
    return redirect('login_view')

def tadjiki(request):
    return render(request, 'prac_APP/Tadjiki.html')