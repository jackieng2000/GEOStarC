from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from collections import Counter

class Command(BaseCommand):
    help = 'Display user registration statistics'

    def handle(self, *args, **options):
        # Get all users
        total_users = User.objects.count()
        
        # Get social accounts
        social_accounts = SocialAccount.objects.all()
        
        # Count by provider
        provider_count = Counter()
        for account in social_accounts:
            provider_count[account.provider] += 1
        
        # Email users
        email_users = total_users - sum(provider_count.values())
        
        # Display results
        self.stdout.write(self.style.SUCCESS(f"Total Users: {total_users}"))
        self.stdout.write(self.style.SUCCESS(f"Email Users: {email_users}"))
        
        for provider, count in provider_count.items():
            self.stdout.write(self.style.SUCCESS(f"{provider.title()} Users: {count}"))
        
        # Percentage calculation
        if total_users > 0:
            self.stdout.write("\nPercentage Breakdown:")
            self.stdout.write(f"Email: {(email_users/total_users)*100:.1f}%")
            for provider, count in provider_count.items():
                percentage = (count/total_users)*100
                self.stdout.write(f"{provider.title()}: {percentage:.1f}%")