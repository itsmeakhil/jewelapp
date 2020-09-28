from django.contrib.auth.base_user import BaseUserManager

from utils.basemanager import BaseManager


class UserManager(BaseUserManager):
    """Class for Custom user manager for abstracting the Django Authuser """
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given user id(Outlook ID) and password.
        """
        if not username:
            raise ValueError('The given user id must be set')
        user = self.model(username=username, **extra_fields)
        user.set_is_admin = True
        user.set_is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)

    def get_user_by_user_name(self, username):
        """Function to get user by user name"""
        return self.filter(username=username).first()

    def delete_user(self, username):
        """function to delete user"""
        return self.get(username=username).delete()

    def get_by_id(self, pk):
        """function to get the objects by passing their id"""
        return self.get(pk=pk)

    def get_all(self):
        """Function to get all users list"""
        return super(UserManager, self).all()

    def get_all_active(self):
        """Function to get all active users list"""
        return self.get_all().filter(is_active=True)

    def get_by_filter(self, **filter_args):
        """Function to get user by filter"""
        return self.get_all_active().filter(**filter_args)

    def does_exist_username(self, query):
        """Function to check if user exists"""
        if self.get_by_filter(username__iexact=query).exists():
            return True
        return False

    def does_exist_phone_number(self, query):
        """Function to check if phone number exists"""
        if self.get_by_filter(phone_number__iexact=query).exists():
            return True
        return False

    def does_exist_email(self, query):
        """Function to check if email exists"""
        if self.get_by_filter(email__iexact=query).exists():
            return True
        return False


class UserTypeManager(BaseManager):
    """Manager class to manage User Types"""

    def get_by_filter(self, **filter_args):
        """Function to get user type  by filter"""
        return self.get_all_active().filter(**filter_args)

    def get_by_search_query(self, query):
        """Function to search and filter using user type name"""
        return self.get_by_filter(user_type__icontains=query)

    def does_exist_user_type(self, query):
        """Function to check if User type exists"""
        if self.get_by_filter(user_type__iexact=query).exists():
            return True
        return False
