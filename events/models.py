# events/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator

User = get_user_model()

class Event(models.Model):
    # Event Type Choices
    EVENT_TYPE_CHOICES = [
        ('T', 'Trail'),
        ('R', 'Race'),
        ('C', 'Casual'),
    ]
    
    # Primary Key (AutoField is default, but we can specify if needed)
    EventId = models.AutoField(primary_key=True)
    
    # Required Fields
    EventName = models.CharField(
        max_length=255,
        verbose_name="Event Name",
        help_text="Required. Enter the name of the event."
    )
    
    AdminUser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='administered_events',
        verbose_name="Admin User",
        help_text="User who created/administered this event"
    )
    
    # File Fields
    GpxFile = models.FileField(
        upload_to='events/gpx_files/',
        blank=True,
        null=True,
        verbose_name="GPX File",
        help_text="Upload GPX file for the event route"
    )
    
    # Numeric Fields with defaults
    Enrolled = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Number of Enrolled Users",
        help_text="Total number of users enrolled in this event"
    )
    
    Distance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name="Distance (km)",
        help_text="Total distance of the event in kilometers"
    )
    
    Elevation = models.IntegerField(
        default=0,
        verbose_name="Elevation Gain (m)",
        help_text="Total elevation gain in meters"
    )
    
    # Location Fields
    Country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Country",
        help_text="Country where the event takes place"
    )
    
    # Timestamps
    CreateTimeStamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creation Timestamp"
    )
    
    StartTimestamp = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Event Start Time",
        help_text="Scheduled start time of the event"
    )
    
    EndTimestamp = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Event End Time",
        help_text="Scheduled end time of the event"
    )
    
    # Status Fields
    Active = models.BooleanField(
        default=False,
        verbose_name="Active Status",
        help_text="Whether the event is currently active"
    )
    
    Type = models.CharField(
        max_length=1,
        choices=EVENT_TYPE_CHOICES,
        default='C',
        verbose_name="Event Type",
        help_text="Type of event: Trail, Race, or Casual"
    )
    
    # Additional useful fields
    Description = models.TextField(
        blank=True,
        verbose_name="Event Description",
        help_text="Detailed description of the event"
    )
    
    MaxParticipants = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Maximum Participants",
        help_text="Maximum number of participants allowed (optional)"
    )
    
    Location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Location",
        help_text="Specific location or venue of the event"
    )
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-CreateTimeStamp']
        indexes = [
            models.Index(fields=['Active']),
            models.Index(fields=['Type']),
            models.Index(fields=['StartTimestamp']),
            models.Index(fields=['AdminUser']),
        ]
    
    def __str__(self):
        return f"{self.EventName} ({self.get_Type_display()})"
    
    def is_upcoming(self):
        """Check if event is in the future"""
        if self.StartTimestamp:
            return self.StartTimestamp > timezone.now()
        return False
    
    def is_ongoing(self):
        """Check if event is currently ongoing"""
        now = timezone.now()
        if self.StartTimestamp and self.EndTimestamp:
            return self.StartTimestamp <= now <= self.EndTimestamp
        return False
    
    def is_past(self):
        """Check if event has ended"""
        if self.EndTimestamp:
            return self.EndTimestamp < timezone.now()
        return False
    
    def get_duration(self):
        """Calculate event duration in hours"""
        if self.StartTimestamp and self.EndTimestamp:
            duration = self.EndTimestamp - self.StartTimestamp
            return round(duration.total_seconds() / 3600, 2)
        return None
    
    def can_enroll(self):
        """Check if users can still enroll in this event"""
        if self.MaxParticipants and self.Enrolled >= self.MaxParticipants:
            return False
        if self.StartTimestamp and self.StartTimestamp <= timezone.now():
            return False
        return self.Active
    
    def save(self, *args, **kwargs):
        # Auto-update Active status based on timestamps
        if self.StartTimestamp and self.EndTimestamp:
            now = timezone.now()
            self.Active = self.StartTimestamp <= now <= self.EndTimestamp
        
        super().save(*args, **kwargs)


class EventAdmin(models.Model):
    """
    Additional administrators for an event (besides the main AdminUser)
    """
    EventId = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='additional_admins',
        verbose_name="Event"
    )
    
    UserId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_admin_roles',
        verbose_name="Admin User"
    )
    
    # Timestamp for when the user was made an admin
    AssignedTimestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Assigned Timestamp"
    )
    
    # Role or permissions level (optional)
    Role = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Admin Role",
        help_text="Optional role description (e.g., 'Co-Organizer', 'Moderator')"
    )
    
    class Meta:
        verbose_name = "Event Administrator"
        verbose_name_plural = "Event Administrators"
        unique_together = ['EventId', 'UserId']
        ordering = ['-AssignedTimestamp']
    
    def __str__(self):
        return f"{self.UserId.username} - {self.EventId.EventName} Admin"


class EventUser(models.Model):
    """
    Users enrolled in events with their participation details
    """
    EventId = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='enrolled_users',
        verbose_name="Event"
    )
    
    UserId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_participations',
        verbose_name="User"
    )
    
    # Participation timestamps
    StartTimestamp = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Participation Start Time",
        help_text="When the user started the event"
    )
    
    EndTimestamp = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Participation End Time",
        help_text="When the user completed the event"
    )
    
    NetTime = models.DurationField(
        blank=True,
        null=True,
        verbose_name="Net Time",
        help_text="Net time taken to complete the event (HH:MM:SS)"
    )
    
    # Enrollment timestamp
    EnrolledTimestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Enrollment Timestamp"
    )
    
    # Status fields
    Completed = models.BooleanField(
        default=False,
        verbose_name="Completed",
        help_text="Whether the user has completed the event"
    )
    
    # Additional tracking fields
    DistanceCompleted = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name="Distance Completed (km)",
        help_text="Distance completed by the user in kilometers"
    )
    
    Notes = models.TextField(
        blank=True,
        verbose_name="Participation Notes",
        help_text="Any notes about the user's participation"
    )
    
    class Meta:
        verbose_name = "Event Participant"
        verbose_name_plural = "Event Participants"
        unique_together = ['EventId', 'UserId']
        ordering = ['-EnrolledTimestamp']
        indexes = [
            models.Index(fields=['EventId', 'UserId']),
            models.Index(fields=['Completed']),
            models.Index(fields=['StartTimestamp']),
        ]
    
    def __str__(self):
        return f"{self.UserId.username} - {self.EventId.EventName}"
    
    def calculate_net_time(self):
        """Calculate net time if both start and end timestamps are available"""
        if self.StartTimestamp and self.EndTimestamp:
            self.NetTime = self.EndTimestamp - self.StartTimestamp
            return self.NetTime
        return None
    
    def is_active_participant(self):
        """Check if user is currently participating (started but not finished)"""
        return self.StartTimestamp is not None and self.EndTimestamp is None
    
    def save(self, *args, **kwargs):
        # Auto-calculate net time if both timestamps are provided
        if self.StartTimestamp and self.EndTimestamp:
            self.calculate_net_time()
            self.Completed = True
        
        # Update event enrollment count
        if self.pk is None:  # New enrollment
            self.EventId.Enrolled += 1
            self.EventId.save()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Update event enrollment count on deletion
        self.EventId.Enrolled -= 1
        self.EventId.save()
        super().delete(*args, **kwargs)