import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'check_spam.settings')
import django
django.setup()

from users.models import User, Contact, Spam, SpamMarkedBy

def populate():
    # Create users
    user1 = User.objects.create_user(username='aaaaa', phone_number='11111111', password='pass123')
    user2 = User.objects.create_user(username='bbbbb', phone_number='2222222', password='word456')

    # Create contacts for user1
    contact1 = Contact.objects.create(owner=user1, name='sagar', phone_number='233333', email='sagar@email.com')
    contact2 = Contact.objects.create(owner=user1, name='sahil', phone_number='2225555', email='sahil@email.com')

    # Create contacts for user2
    contact3 = Contact.objects.create(owner=user2, name='xyz', phone_number='333566', email='xyz@email.com')

    # Create spam entries
    spam1 = Spam.objects.create(phone_number='111244777')
    spam2 = Spam.objects.create(phone_number='333488886')

    # Users marking phone numbers as spam
    SpamMarkedBy.objects.create(spam=spam1, user=user1)
    SpamMarkedBy.objects.create(spam=spam2, user=user2)

    print("Sample data added successfully.")

if __name__ == '__main__':
    populate()
