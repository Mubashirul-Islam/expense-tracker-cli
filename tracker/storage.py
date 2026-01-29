"""
Storage layer for expense data persistence.
"""

import json
import logging
from pathlib import Path
from typing import List, Optional
from tracker.models import Expense

logger = logging.getLogger(__name__)


class ExpenseStorage:
    """Handles reading and writing expenses to JSON file."""
    
    def __init__(self, filepath: str = "data/expenses.json"):
        """
        Initialize storage with filepath.
        
        Args:
            filepath: Path to JSON file for storing expenses
        """
        self.filepath = Path(filepath)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the data file and directory if they don't exist."""
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            
            if not self.filepath.exists():
                self.filepath.write_text("[]")
                logger.info(f"Created new expenses file: {self.filepath}")
        except Exception as e:
            logger.error(f"Error creating file {self.filepath}: {e}")
            raise
    
    def load_expenses(self) -> List[Expense]:
        """
        Load all expenses from file.
        
        Returns:
            List of Expense objects
            
        Raises:
            Exception: If file cannot be read or parsed
        """
        try:
            data = self.filepath.read_text()
            expenses_data = json.loads(data)
            expenses = [Expense.from_dict(exp) for exp in expenses_data]
            #logger.info(f"Loaded {len(expenses)} expenses from {self.filepath}")
            return expenses
        except json.JSONDecodeError as e:
            logger.error(f"Corrupted JSON file {self.filepath}: {e}")
            raise Exception(f"Error: Corrupted data file. Please check {self.filepath}")
        except Exception as e:
            logger.error(f"Error reading expenses file: {e}")
            raise Exception(f"Error: Could not read expenses file: {e}")
    
    def save_expenses(self, expenses: List[Expense]):
        """
        Save all expenses to file.
        
        Args:
            expenses: List of Expense objects to save
            
        Raises:
            Exception: If file cannot be written
        """
        try:
            expenses_data = [exp.to_dict() for exp in expenses]
            data = json.dumps(expenses_data, indent=2)
            self.filepath.write_text(data)
            logger.info(f"Saved {len(expenses)} expenses to {self.filepath}")
        except Exception as e:
            logger.error(f"Error writing expenses file: {e}")
            raise Exception(f"Error: Could not save expenses: {e}")
    
    def add_expense(self, expense: Expense):
        """
        Add a single expense to storage.
        
        Args:
            expense: Expense object to add
        """
        expenses = self.load_expenses()
        expenses.append(expense)
        self.save_expenses(expenses)
        #logger.info(f"Added expense: {expense.id}")
    
    def get_all_ids(self) -> List[str]:
        """
        Get all existing expense IDs.
        
        Returns:
            List of expense IDs
        """
        try:
            expenses = self.load_expenses()
            return [exp.id for exp in expenses]
        except Exception:
            return []
    
    def delete_expense(self, expense_id: str) -> bool:
        """
        Delete an expense by ID.
        
        Args:
            expense_id: ID of expense to delete
            
        Returns:
            True if deleted, False if not found
        """
        expenses = self.load_expenses()
        original_count = len(expenses)
        expenses = [exp for exp in expenses if exp.id != expense_id]
        
        if len(expenses) < original_count:
            self.save_expenses(expenses)
            #logger.info(f"Deleted expense: {expense_id}")
            return True
        return False
    
    def update_expense(self, expense_id: str, updates: dict) -> Optional[Expense]:
        """
        Update an expense by ID.
        
        Args:
            expense_id: ID of expense to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Expense object or None if not found
        """
        expenses = self.load_expenses()
        
        for i, exp in enumerate(expenses):
            if exp.id == expense_id:
                # Update fields
                exp_dict = exp.to_dict()
                exp_dict.update(updates)
                expenses[i] = Expense.from_dict(exp_dict)
                self.save_expenses(expenses)
                #logger.info(f"Updated expense: {expense_id}")
                return expenses[i]
        
        return None
