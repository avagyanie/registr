import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))

        if len(re.findall(r'[A-Z]', password)) < 3:
            raise ValidationError(_('Password must contain at least 3 uppercase letters.'))

        if len(re.findall(r'[a-z]', password)) < 3:
            raise ValidationError(_('Password must contain at least 3 lowercase letters.'))

        if len(re.findall(r'[^A-Za-z0-9]', password)) < 3:
            raise ValidationError(_('Password must contain at least 3 special characters.'))

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, 3 uppercase letters, "
            "3 lowercase letters, and 3 special characters."
        )
