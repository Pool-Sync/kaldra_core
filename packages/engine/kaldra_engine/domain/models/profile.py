"""
Profile model for Supabase.
"""
from dataclasses import dataclass
from typing import Optional
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
    created_at: Optional[datetime] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    role: Optional[str] = None
    notes: Optional[str] = None
