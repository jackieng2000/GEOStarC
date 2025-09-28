import os
import django
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rbackend.settings')
django.setup()

try:
    send_mail(
        'Test Email from Django - Gmail Setup',
        'Congratulations! Your Gmail configuration is working successfully.\n\n'
        'This email was sent from your Django application using Gmail SMTP.',
        'noreply@jackieng.hk',
        ['jackieng2000@yahoo.com.hk'],  # Replace with your test email
        fail_silently=False,
    )
    print("Test email sent! Check your jackieng2000@yahoo.com.hk inbox.")
except Exception as e:
    print(f"❌ Error sending email: {e}")