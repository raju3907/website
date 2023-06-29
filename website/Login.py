import datetime
import traceback
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
            print("checking Process of Middleware")
            if "signin" in str(request):
                print('contains signin or signup')
                return None
            elif 'signup' in str(request):
                return None
            elif 'welcome' in str(request):
                return None
            elif "Authorization" in request.headers:
                print('contains authorization')
                access_=request.headers.get('Authorization')
                decode_json=jwt.decode(access_,settings.SECRET_KEY,algorithms='HS256')
                id_=decode_json["username"]
                try:
                    user=USERS.objects.get(username=id_)
                    if decode_json['exp']<=datetime.datetime.utcnow():
                        return None
                    else:
                        return HttpResponse("Please login again")
                except:
                    return HttpResponse("User not valid")
            else:
                print('no',request,request.headers)
                return HttpResponse("Authorization Failed")
        except:
            traceback.print_exc()
            return HttpResponse("Authorization Failed")