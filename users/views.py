import re
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer, UserSerializerWithToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from .models import User, PhoneOTP
from datetime import timedelta
from random import randint
from datetime import datetime
import pytz
from django.contrib.auth.hashers import check_password

# Create your views here.
@api_view(['GET',])
@permission_classes([permissions.IsAuthenticated,])
def user_profile(request):
    user = request.user
    try:
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        return Response({'message': 'something is wrong!', 'status': status.HTTP_400_BAD_REQUEST})


@api_view(['GET',])
@permission_classes([permissions.IsAdminUser,])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


utc = pytz.UTC


def validate_phone(phone):
    pattern = re.compile("^09[0|1|2|3][0-9]{8}$", re.IGNORECASE)
    return pattern.match(phone) is not None


def get_otp_code(phone):
    if phone:
        key = randint(99999, 999999)
        print(key)
        return key
    else:
        return False



# def send_otp_code(phone, code):
#     print(code)


@api_view(['POST'])
def verify_phone_send_otp_code(request):
    phone_number = request.data.get('phone')

    if phone_number:
        phone = str(phone_number)

        if validate_phone(phone):
            user = User.objects.filter(phone__iexact=phone)

            if user.exists():
                return Response({'detail': 'An account with this phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                key = get_otp_code(phone)

                if key:
                    phone_otp = PhoneOTP.objects.filter(phone__iexact=phone)
                    now = datetime.now().replace(tzinfo=utc)

                    if phone_otp.exists():
                        phone_otp = phone_otp.first()
                        created_at = phone_otp.created_at.replace(tzinfo=utc)
                        obj_expiration_date = created_at + timedelta(days=1)

                        if now > obj_expiration_date:
                            phone_otp.delete()

                            new_phone_otp = PhoneOTP.objects.create(
                                phone = phone,
                                otp = str(key),
                                resend_at = now + timedelta(minutes=2),
                                expire_at = now + timedelta(minutes=2)
                            )

                            # send_otp_code(phone[1:], str(key))

                            return Response({'detail': 'Six digit code has been set to your phone number', 'phone': phone, 'resend_at': new_phone_otp.resend_at, 'expire_at': new_phone_otp.expire_at})
                        else:
                            count = phone_otp.count

                            if count <= 10:
                                resend_at = phone_otp.resend_at.replace(tzinfo=utc)

                                if now > resend_at:
                                    phone_otp.otp = str(key)
                                    phone_otp.resend_at = now + timedelta(minutes=3)
                                    phone_otp.expire_at = now + timedelta(minutes=3)
                                    phone_otp.count = count + 1
                                    phone_otp.save()

                                    # send_otp_code(phone[1:], str(key))

                                    return Response({'detail': 'Six digit code has been set to your phone numbe', 'phone': phone, 'resend_at': phone_otp.resend_at, 'expire_at': phone_otp.expire_at})                
                                else:
                                    return Response({'detail': 'Please wait for a resend'}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response({'detail': 'You are not allowed to get otp code for 24 hours'}, status=status.HTTP_403_FORBIDDEN)
                    else:
                        new_phone_otp = PhoneOTP.objects.create(
                            phone = phone,
                            otp = str(key),
                            resend_at = now + timedelta(minutes=3),
                            expire_at = now + timedelta(minutes=3)
                        )

                        # send_otp_code(phone[1:], str(key))

                        return Response({'detail': 'Six digit code has been set to your phone numbe', 'phone': phone, 'resend_at': new_phone_otp.resend_at, 'expire_at': new_phone_otp.expire_at})
                else:
                    return Response({'detail': 'Something wrong when sending the code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'detail': 'Entered phone number is wrong'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Please enter your phone number'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp(request):
    phone_number = request.data.get('phone')
    sent_otp = request.data.get('otp')

    if phone_number and sent_otp:
        phone = str(phone_number)

        if validate_phone(phone):
            phone_otp = PhoneOTP.objects.filter(phone__iexact=phone)

            if phone_otp.exists():
                phone_otp = phone_otp.first()
                otp = phone_otp.otp
                now = datetime.now().replace(tzinfo=utc)
                expire_at = phone_otp.expire_at.replace(tzinfo=utc)

                if now <= expire_at:
                    if str(sent_otp) == str(otp):
                        phone_otp.is_validated = True
                        phone_otp.save()
                        return Response({'detail': 'Successfully confirmed the code'})
                    else:
                        return Response({'detail': 'Entered OTP is wrong'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'detail': 'Code has been expired. Please go back and resend.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({'detail': 'First you should verify your phone number'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'detail': 'Entered phone number is wrong'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Please enter phone number and otp code'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    phone_number = request.data.get('phone')
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    if phone_number and name and email and password:
        phone = str(phone_number)

        if validate_phone(phone):
            phone_otp = PhoneOTP.objects.filter(phone__iexact=phone)
            user = User.objects.filter(phone__iexact=phone)

            if user.exists():
                return Response({'detail': 'An account with this phone number already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                if phone_otp.exists():
                    phone_otp = phone_otp.first()

                    if phone_otp.is_validated:
                        password = str(password)
                        if len(password) >= 5:
                            user = User.objects.create_user(
                                phone = phone,
                                name = str(name),
                                email = email
                            )
                            user.set_password(password)
                            user.logged_in = True
                            user.save()

                            serializer = UserSerializerWithToken(user, many=False)
                            return Response(serializer.data)
                        else:
                            return Response({'detail': 'You should provide a password with at least 5 characters'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    else:
                        return Response({'detail': 'First you should verify OTP code'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({'detail': 'You should verify your phone number first'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'detail': 'Entered phone number is wrong'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Please enter your phone, name, email and password'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login(request):
    phone_number = request.data.get('phone')
    password = request.data.get('password')

    if phone_number:
        phone = str(phone_number)
        
        if validate_phone(phone):                
            user = User.objects.filter(phone__iexact=phone)

            if user.exists():
                user = user.first()

                if user.check_password(password):
                    user.logged_in = True
                    user.save()

                    serializer = UserSerializerWithToken(user, many=False)

                    return Response(serializer.data)
                else:
                    return Response({'detail': 'Entered password is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'No account found with this phone number'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'detail': 'Entered phone number is wrong'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Please enter your phone number and password'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    user_id = request.user.id

    if user_id:
        user = User.objects.filter(pk=user_id)

        if user.exists():
            user = user.first()
            user.logged_in = False
            user.save()

            phone_otp = PhoneOTP.objects.filter(phone__iexact=user.phone)

            if phone_otp.exists():
                phone_otp = phone_otp.first()
                phone_otp.is_validated = False
                phone_otp.save()

            return Response({'detail': 'Logout successfully'})
        else:
            return Response({'detail': 'User doesnt exist'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'detail': 'You should provide correct user token in the request header'})