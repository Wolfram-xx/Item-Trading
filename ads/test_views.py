import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal, Status, Categories, Conditions

@pytest.mark.django_db
def test_user_registration(client):
    response = client.post('/reg/', {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'password_again': 'password123',
    })
    assert response.status_code == 302
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_login_success(client, django_user_model):
    user = django_user_model.objects.create_user(username='test', password='pass')
    response = client.post('/login/', {
        'username': 'test',
        'password': 'pass',
    })
    assert response.status_code == 302

@pytest.mark.django_db
def test_create_ad(client, django_user_model):
    user = django_user_model.objects.create_user(username='user1', password='pass')
    client.login(username='user1', password='pass')
    response = client.post('/new_item/create/', {
        'title': 'Test Ad',
        'descript': 'Test Description',
        'url': 'https://example.com/image.jpg',
        'category': Categories.CARS,
        'condition': Conditions.NEW
    })
    assert response.status_code == 302
    assert Ad.objects.filter(title='Test Ad').exists()

@pytest.mark.django_db
def test_create_trade(client, django_user_model):
    sender = django_user_model.objects.create_user(username='sender', password='1234')
    receiver = django_user_model.objects.create_user(username='receiver', password='1234')
    ad = Ad.objects.create(
        user=receiver.id,
        title='Receiver Ad',
        description='desc',
        image_url='https://example.com/image.jpg',
        category=Categories.ELECT,
        condition=Conditions.NOT_NEW,
    )
    client.login(username='sender', password='1234')
    response = client.post('/market/create_trade/', {
        'ad_id': ad.id,
        'comment': 'Interested in your item'
    })
    assert response.status_code == 302
    assert ExchangeProposal.objects.filter(ad_sender=sender.id, ad_receiver=receiver.id).exists()

@pytest.mark.django_db
def test_accept_trade(client, django_user_model):
    sender = django_user_model.objects.create_user(username='sender', password='1234')
    receiver = django_user_model.objects.create_user(username='receiver', password='1234')
    trade = ExchangeProposal.objects.create(
        ad_sender=sender.id,
        ad_receiver=receiver.id,
        comment='Please accept',
    )
    client.login(username='receiver', password='1234')
    response = client.get(f'/accept_trade/?id={trade.id}')
    trade.refresh_from_db()
    assert response.status_code == 302
    assert trade.status == Status.ACCEPTED