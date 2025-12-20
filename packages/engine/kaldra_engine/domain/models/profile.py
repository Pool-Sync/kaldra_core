"""
Profile model for Supabase.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Profile:
    """
    User profile model.

    Attributes:
        id: Unique identifier
        created_at: Creation timestamp
        email: User email
        display_name: Display name
        role: User role (admin, viewer, beta)
        notes: Additional notes
    """

    id: str
    created_at: datetime | None = None
    email: str | None = None
    display_name: str | None = None
    role: str | None = None
    notes: str | None = None
