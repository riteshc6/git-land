from django import forms
from .models import Ssh_key
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import subprocess


class UserRegistrationForm(UserCreationForm):
    key_name = forms.CharField(label="key name", required=True)
    ssh_key = forms.Textarea(label="ssh key", required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'password2', 'key_name', 'ssh_key')

    def save(self, commit=True):
        user = super().save(commit=False)
        ssh_key = Ssh_key()
        ssh_key.key_name = self.cleaned_data['key_name']
        ssh_key.ssh_key = self.cleaned_data['ssh_key']

        if commit:
            user.save()
            ssh_key.user = user
            ssh_key.save()
            subprocess.run(
                ['./create_user.sh', ssh_key.ssh_key, user.username])
            return user, ssh_key


class RepoForm(forms.Form):
    repo_name = forms.CharField(label="Repo Name", required=True)
