from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Note
from .forms import NoteForm


def home(request):

    notes = Note.objects.all()

    return render(
        request,
        'notes/home.html',
        {'notes': notes}
    )


def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = UserCreationForm()

    return render(
        request,
        'notes/register.html',
        {'form': form}
    )


@login_required
def upload_note(request):

    if request.method == 'POST':

        form = NoteForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            note = form.save(commit=False)

            note.uploaded_by = request.user

            note.save()

            return redirect('home')

    else:

        form = NoteForm()

    return render(
        request,
        'notes/upload_note.html',
        {'form': form}
    )