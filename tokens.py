import cryptography
import random

from datetime import datetime, timedelta
from django.conf import settings

from cryptography.fernet import Fernet


class ExpiringTokenGenerator:
    fernet = Fernet(settings.FERNET_KEY)

    DATE_FORMAT = "%Y-%m-%d %H-%M-%S"

    def _get_time(self):
        """Returns a string with the current UTC time"""
        return datetime.utcnow().strftime(self.DATE_FORMAT)

    def _parse_time(self, d):
        """Parses a string produced by _get_time and returns a datetime object"""
        return datetime.strptime(d, self.DATE_FORMAT)

    def generate_token(self, text):
        """Generates an encrypted token"""
        full_text = text + "|" + self._get_time()
        token = self.fernet.encrypt(bytes(full_text, "utf-8"))

        return token

    def get_token_value(self, token, token_type):
        """Gets a value from an encrypted token.
        Returns None if the token is invalid or has expired.
        """
        try:
            value = self.fernet.decrypt(bytes(token, encoding="utf-8"))
            value = value.decode("utf-8")
            separator_pos = value.rfind("|")

            text = value[:separator_pos]
            token_time = self._parse_time(value[separator_pos + 1 :])
            time = {"minutes": 30}
            if token_time + timedelta(**time) < datetime.utcnow():
                return None

        except cryptography.fernet.InvalidToken:
            return None

        return text

    def is_valid_token(self, token, token_type):
        return self.get_token_value(token, token_type) != None
