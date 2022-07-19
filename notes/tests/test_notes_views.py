from pydoc import cli
from urllib import response
import pytest

from django.contrib.auth.models import User

from notes.models import Notes

@pytest.fixture
def logged_user(client):
    user = User.objects.create_user('John', 'john@test.com', 'pass')
    client.login(username=user.username, password='pass')
    return user
    

@pytest.mark.django_db
def test_list_endpoint_returns_user_notes(client, logged_user):
    
    '''
		Creating two notes for the client
    '''
    Notes.objects.create(title='Test Note 1', text='', user=logged_user)
    Notes.objects.create(title='Test Note 2', text='', user=logged_user)
    
    response = client.get(path='/smart/notes')
    assert 200 == response.status_code
    
    content = str(response.content)
    assert 'Test Note 1' in content
    assert 2 == content.count('<h3>')
    
    
@pytest.mark.django_db
def test_list_endpoint_only_notes_from_aunthenticated_user(client, logged_user):
    new_user = User.objects.create_user('Alex', 'alex@test.com', 'pass123')
    Notes.objects.create(title='New Test Note', text='', user=new_user)
    
    
    Notes.objects.create(title='Test Note 1', text='', user=logged_user)
    Notes.objects.create(title='Test Note 2', text='', user=logged_user)
    
    '''
		Creating two notes for the client
    '''
    
    response = client.get(path='/smart/notes')
    assert 200 == response.status_code
    
    
    content = str(response.content)
    assert 'New Test Note' not in content
    assert 2 == content.count('<h3>')