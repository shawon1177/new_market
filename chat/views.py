from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message

@login_required
def init_chat(request, user_id):
    User = get_user_model()

    other_user = get_object_or_404(User, id=user_id)

    conversation = Conversation.objects.filter(users=request.user).filter(users=other_user).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.users.add(request.user, other_user)

    return redirect('chat_room', convo_id=conversation.id)

@login_required
def chat_room(request, convo_id):
    conversation = get_object_or_404(Conversation, id=convo_id)

    # security: only allowed users
    if request.user not in conversation.users.all():
        return redirect('food_list')

    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

    if request.method == "POST":
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            text=request.POST.get('text')
        )
        return redirect('chat_room', convo_id=convo_id)

    return render(request, 'chat/chat_room.html', {
        'conversation': conversation,
        'messages': messages
    })