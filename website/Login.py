import datetime
import traceback

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import jwt
from .models import USERS
from django.http import HttpResponse
def access_token(username):
    try:
        access={
            "username":username,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(days=2),
            'iat':datetime.datetime.utcnow()
        }
        access_=jwt.encode(access,settings.SECRET_KEY,algorithm="HS256")
        return access_
    except:
        traceback.print_exc()
class AuthMiddleware(MiddlewareMixin):
    def process_view(self,request,view_func,*view_args,**view_kwargs):
        try:
            access_=request.COOKIES.get('Authorization')

            if "signin" in str(request):
                if access_=="":
                    return None
                else:
                    return redirect('Home')
            elif 'signup' in str(request):
                if access_=="":
                    return None
                else:
                    return redirect('Home')
            elif 'welcome' in str(request):
                if access_=="":
                    return None
                else:
                    return redirect('Home')
            elif 'signout' in str(request):

                # print(request.COOKIES.get('Authorization'))
                # request.delete_cookie('Authorization')
                return None
            elif "Authorization" in request.COOKIES:
                decode_json=jwt.decode(access_,settings.SECRET_KEY,algorithms='HS256')
                id_=decode_json["username"]
                try:
                    user=USERS.objects.get(username=id_)
                    dd=datetime.datetime.utcfromtimestamp(decode_json['exp'])
                    if dd >= datetime.datetime.utcnow():
                        return None
                    else:
                        return redirect('signin')
                except:
                    return redirect('signin')
            else:
                return redirect('signin')
        except:
            traceback.print_exc()
            return redirect('signin')