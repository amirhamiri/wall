import string
from random import randint

from django.core.cache import cache
import datetime


class OTP:

    def __init__(self):
        self.otp_expiry_minutes = 2

    def generate_otp(self, phone):
        otp = randint(1000, 9999)
        cache.set(phone, (otp, datetime.datetime.now()), self.otp_expiry_minutes * 60)
        print(otp)
        return otp

    def verify_otp(self, otp, phone):
        stored_otp, timestamp = cache.get(phone)
        if stored_otp == otp:
            if datetime.datetime.now() - timestamp > datetime.timedelta(minutes=self.otp_expiry_minutes):
                return True
            return False    
        else:
            return False

    def clear_otp(self, phone):
        cache.delete(phone)

    def send_otp(self, otp, phone):
        # Send OTP to the phone number

        pass