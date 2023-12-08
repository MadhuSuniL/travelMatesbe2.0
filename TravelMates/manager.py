from django.contrib.auth.models import BaseUserManager
from helper.Funtions import Print,get_travel_mate_id


class TravelMateManager(BaseUserManager):
    def create_travel_mate(self,email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not phone:
            raise ValueError("The Phone field must be set") 
        extra_fields['is_verified'] = True
        
        email = self.normalize_email(email)
        travel_mate = self.model(travel_mate_id = get_travel_mate_id(), phone = phone, email=email, **extra_fields)
        Print(password)
        travel_mate.set_password(password)
        travel_mate.save(using=self._db)
        return travel_mate

    def create_supertravelmate(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        extra_fields['is_verified'] = True
        return self.create_travel_mate(email, phone, password, **extra_fields)

    def create_superuser(self, email, phone, password=None, **extra_fields):
        return self.create_supertravelmate(email, phone, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset()

    def active_travel_mates(self):
        return self.get_queryset().filter(is_active=True)

    def verified_travel_mates(self):
        return self.active_travel_mates().filter(is_verified=True)

    def get_active_travel_mate(self, **kwargs):
        return self.active_travel_mates().get(**kwargs)

    def get_verified_travel_mate(self, **kwargs):
        return self.verified_travel_mates().get(**kwargs)

    def all(self, **kwargs):
        return self.verified_travel_mates()
        
    def authenticate(self, phone, password):
        try:
            travel_mate = self.all().get(phone = phone)
            if travel_mate.check_password(password):
                return travel_mate
            else:
                Print(travel_mate)
                return None             
        except Exception as e:
            Print()

            return None    
                
    def change_password(self,travel_mate,old_password,new_password):
        if travel_mate.check_password(old_password):
            travel_mate.set_password(new_password)
            travel_mate.save()
            return True
        else:
            raise Exception('Invalid old password!')
        
        
        
        
        