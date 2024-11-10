from django.contrib.auth.decorators import user_passes_test
from kavenegar import *

def send_sms(phone_number,code):
    try:
        api = KavenegarAPI('482B764F6B3876696654796774384B2B4D5543727944547270746659574B7A4E765432624177586678706B3D')
        params  = {
            'sender': '',
			'receptor': phone_number,
			'message': f'{code} کد تایید شما '
        }
        res = api.sms_send(params)
        print(res)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


# @user_passes_test
def test_func(user):
    return user.is_authenticated and user.is_admin
        