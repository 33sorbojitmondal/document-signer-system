from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from signer.crypto_utils import generate_rsa_key_pair, serialize_private_key, serialize_public_key
from signer.models import UserProfile


class Command(BaseCommand):
    help = 'Create the default authority account with RSA key pair'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='authority')
        parser.add_argument('--password', default='authority123')
        parser.add_argument('--email', default='authority@docsigner.edu')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        if User.objects.filter(username=username).exists():
            profile = User.objects.get(username=username).profile
            if profile.role != 'authority':
                profile.role = 'authority'
                profile.save()
            self.stdout.write(self.style.WARNING(f'Authority user "{username}" already exists.'))
            return

        user = User.objects.create_user(username=username, email=email, password=password)
        private_key, public_key = generate_rsa_key_pair()
        UserProfile.objects.create(
            user=user,
            role='authority',
            private_key=serialize_private_key(private_key),
            public_key=serialize_public_key(public_key),
        )
        self.stdout.write(self.style.SUCCESS(f'Authority account created: {username} / {password}'))
