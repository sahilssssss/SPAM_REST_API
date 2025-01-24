from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer, CharField
from .models import Spam , Contact



# SERIALIZER
class UserRegistrationSerializer(Serializer):
    username = CharField(max_length=150)
    password = CharField(write_only=True)
    phone_number = CharField(max_length=15)
    

class MarkSpamSerializer(Serializer):
    phone_number = CharField(max_length=15)

class SearchByNameSerializer(Serializer):
    query = CharField(max_length=150)

class SearchByPhoneNumberSerializer(Serializer):
    phone_number = CharField(max_length=15)




class UserRegistration(APIView):
    def post(self, request):
        print("Request Data:", request.data) 
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            print("Valid Data:", serializer.validated_data)
            user_data = serializer.validated_data
            user = get_user_model().objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                phone_number=user_data['phone_number']
                
            )
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkSpam(APIView):
    def post(self, request):
       
        serializer = MarkSpamSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            
           
            spam_entry, created = Spam.objects.get_or_create(phone_number=phone_number)
            
            
            return Response({'message': 'Phone number marked as spam'}, status=status.HTTP_201_CREATED)
        
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchByName(APIView):
    def get(self, request):
        query = request.query_params.get('query', '') 
        
        if query:
           
            users = get_user_model().objects.filter(username__icontains=query)
            contacts = Contact.objects.filter(name__icontains=query)  
            
            results = []
            
            
            for user in users:
                spam_likelihood = Spam.objects.filter(phone_number=user.phone_number).exists()
                results.append({
                    'name': user.username,
                    'phone_number': user.phone_number,
                    'spam_likelihood': spam_likelihood
                })
            
            
            for contact in contacts:
                spam_likelihood = Spam.objects.filter(phone_number=contact.phone_number).exists()
                results.append({
                    'name': contact.name,
                    'phone_number': contact.phone_number,
                    'spam_likelihood': spam_likelihood
                })
            
            return Response(results, status=status.HTTP_200_OK)
        
        return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
    

class SearchByPhoneNumber(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number', '')
        
        if phone_number:
           
            users = get_user_model().objects.filter(phone_number=phone_number)
            contacts = Contact.objects.filter(phone_number=phone_number)  # Searching contacts by phone number
            
            results = []
            
            
            for user in users:
                spam_likelihood = Spam.objects.filter(phone_number=user.phone_number).exists()
                results.append({
                    'name': user.username,
                    'phone_number': user.phone_number,
                    'spam_likelihood': spam_likelihood
                })
            
            
            for contact in contacts:
                spam_likelihood = Spam.objects.filter(phone_number=contact.phone_number).exists()
                results.append({
                    'name': contact.name,
                    'phone_number': contact.phone_number,
                    'spam_likelihood': spam_likelihood
                })
            
            return Response(results, status=status.HTTP_200_OK)
        
        return Response({'message': 'No phone number provided'}, status=status.HTTP_400_BAD_REQUEST)    