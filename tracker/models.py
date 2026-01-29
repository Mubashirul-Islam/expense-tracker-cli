"""
Data models for the expense tracker.
"""

from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Expense:
    """Represents a single expense entry."""
    id: str
    date: str  # YYYY-MM-DD format
    category: str
    amount: float
    note: str = ""
    currency: str = "BDT"
    created_at: str = datetime.now().isoformat(timespec='seconds')
    
    def to_dict(self) -> dict:
        """Convert expense to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Expense':
        """Create expense from dictionary."""
        return cls(**data)
    
    def __str__(self) -> str:
        """String representation for display."""
        return f"{self.id} | {self.date} | {self.category:15s} | {self.amount:10.2f} {self.currency} | {self.note}"


