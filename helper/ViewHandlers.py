from django.conf import settings
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, ErrorDetail
from rest_framework.views import exception_handler


class CustomViewHandler():
    """_summary_:
        Aim is to add 'perm_key' class  attibute and to handle the exceptions;
    """
    def get_verbose_name(self,key):
        try:
            model=self.queryset.__dict__['model']
            return model._meta.get_field(key).verbose_name
        except KeyError:
            return model._meta.get_field(key).verbose_name
        except:
            return key


    def handle_exception(self, exc):
        response = exception_handler(exc, "context")
        if settings.CUSTOM_VIEW_HANDLING and isinstance(exc, Exception):
            try:status=exc.status_code
            except:status=400
            error=""
            try:
                if isinstance(exc,ValidationError):
                    for key,value in exc.detail.items():
                        if isinstance(value[0], ErrorDetail):
                            if key in ['non_field_errors',]:
                                error=error+""+value[0]+", "
                            else:
                                error=error+str(self.get_verbose_name(key)).replace('_',' ').upper()+" : "+value[0]+", "
                                break
                    error=error[:-2]
                else:
                    error=str(exc)
            except Exception as e:
                error=(str(exc))
            if error == "":
                error=str(exc)
            return Response({"detail":error},status=status,exception=True)
        return super().handle_exception(exc)
    
