from django.db import models
from django.conf import settings
from open_humans.models import OpenHumansMember
import requests


class FitbitMember(models.Model):
    """
    Store OAuth2 data for a Fitbit Member.
    This is a one to one relationship with a OpenHumansMember object.
    """
    user = models.OneToOneField(OpenHumansMember, on_delete=models.CASCADE)
    userid = models.CharField(max_length=255, unique=True, null=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_in = models.CharField(max_length=255)
    scope = models.CharField(max_length=500)
    token_type = models.CharField(max_length=255)

    @classmethod
    def refresh_tokens(self):
        """
        Refresh access token.
        """
        print("calling refresh token method in class")
        response = requests.post(
            'https://api.fitbit.com/oauth2/token',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token},
            auth=requests.auth.HTTPBasicAuth(
                settings.FITBIT_CLIENT_ID, settings.FITBIT_CLIENT_SECRET))
        print(response.text)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            self.token_expires = self.get_expiration(data['expires_in'])
            self.save()
