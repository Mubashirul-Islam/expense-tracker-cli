"""
Business logic layer for expense operations.
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional
from tracker.utils import validate_date, validate_amount, generate_expense_id
from tracker.models import Expense
from tracker.storage import ExpenseStorage

logger = logging.getLogger(__name__)


class ExpenseService:
    """Business logic for expense operations."""
    
    def __init__(self, storage: ExpenseStorage):
        """
        Initialize service with storage.
        
        Args:
            storage: ExpenseStorage instance
        """
        self.storage = storage
    
    def add_expense(
        self,
        date: Optional[str] = None,
        category: str = "",
        amount: float = 0.0,
        note: str = "",
        currency: str = "BDT"
    ) -> Expense:
        """
        Add a new expense.
        
        Args:
            date: Date in YYYY-MM-DD format (default: today)
            category: Expense category
            amount: Expense amount
            note: Optional note
            currency: Currency code (default: BDT)
            
        Returns:
            Created Expense object
            
        Raises:
            ValueError: If validation fails
        """
        # Use today's date if not provided
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Validate inputs
        date = validate_date(date)
        amount = validate_amount(amount)
        category = category.strip().lower()
        
        if not category:
            raise ValueError("category is required")
        
        # Generate unique ID
        existing_ids = self.storage.get_all_ids()
        expense_id = generate_expense_id(date, existing_ids)
        
        # Create and save expense
        expense = Expense(
            id=expense_id,
            date=date,
            category=category,
            amount=amount,
            note=note,
            currency=currency
        )
        
        self.storage.add_expense(expense)
        logger.info(f"Added expense: {expense_id}")
        
        return expense
    
    def list_expenses(
        self,
        month: Optional[str] = None,
        category: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        sort_by: str = "date",
        descending: bool = False,
        limit: Optional[int] = None
    ) -> List[Expense]:
        """
        List expenses with optional filters.
        
        Args:
            month: Filter by month (YYYY-MM format)
            category: Filter by category
            min_amount: Minimum amount filter
            max_amount: Maximum amount filter
            from_date: Start date filter (YYYY-MM-DD)
            to_date: End date filter (YYYY-MM-DD)
            sort_by: Field to sort by (date, amount, category)
            descending: Sort in descending order
            limit: Maximum number of results
            
        Returns:
            List of filtered and sorted Expense objects
        """
        expenses = self.storage.load_expenses()
        
        # Apply filters
        filtered = self._apply_filters(
            expenses,
            month=month,
            category=category,
            min_amount=min_amount,
            max_amount=max_amount,
            from_date=from_date,
            to_date=to_date
        )
        
        # Sort
        if sort_by == "amount":
            filtered.sort(key=lambda x: x.amount, reverse=descending)
        elif sort_by == "category":
            filtered.sort(key=lambda x: x.category, reverse=descending)
        else:  # date
            filtered.sort(key=lambda x: x.date, reverse=descending)
        
        # Limit
        if limit:
            filtered = filtered[:limit]
        
        logger.info(f"Listed {len(filtered)} expenses with filters")
        return filtered
    
    def summary(
        self,
        month: Optional[str] = None,
        category: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict:
        """
        Generate expense summary with totals.
        
        Args:
            month: Filter by month (YYYY-MM format)
            category: Filter by category
            from_date: Start date filter (YYYY-MM-DD)
            to_date: End date filter (YYYY-MM-DD)
            
        Returns:
            Dictionary with count, grand_total, and totals_by_category
        """
        expenses = self.storage.load_expenses()
        
        # Apply filters
        filtered = self._apply_filters(
            expenses,
            month=month,
            category=category,
            from_date=from_date,
            to_date=to_date
        )
        
        # Calculate totals
        grand_total = sum(exp.amount for exp in filtered)
        
        # Group by category
        category_totals = {}
        for exp in filtered:
            if exp.category not in category_totals:
                category_totals[exp.category] = 0.0
            category_totals[exp.category] += exp.amount
        
        summary_data = {
            "count": len(filtered),
            "grand_total": grand_total,
            "totals_by_category": category_totals,
            "currency": filtered[0].currency if filtered else "BDT"
        }
        
        logger.info(f"Generated summary: {len(filtered)} expenses, total {grand_total}")
        return summary_data
    
    def delete_expense(self, expense_id: str) -> bool:
        """
        Delete an expense by ID.
        
        Args:
            expense_id: ID of expense to delete
            
        Returns:
            True if deleted, False if not found
        """
        result = self.storage.delete_expense(expense_id)
        if result:
            logger.info(f"Deleted expense: {expense_id}")
        else:
            logger.warning(f"Expense not found: {expense_id}")
        return result
    
    def edit_expense(self, expense_id: str, **updates) -> Optional[Expense]:
        """
        Edit an expense by ID.
        
        Args:
            expense_id: ID of expense to edit
            **updates: Fields to update
            
        Returns:
            Updated Expense object or None if not found
        """
        # Validate updates
        if "date" in updates:
            updates["date"] = validate_date(updates["date"])
        if "amount" in updates:
            updates["amount"] = validate_amount(updates["amount"])
        if "category" in updates:
            updates["category"] = updates["category"].strip().lower()
        
        result = self.storage.update_expense(expense_id, updates)
        if result:
            logger.info(f"Edited expense: {expense_id}")
        else:
            logger.warning(f"Expense not found: {expense_id}")
        return result
    
    def _apply_filters(
        self,
        expenses: List[Expense],
        month: Optional[str] = None,
        category: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[Expense]:
        """
        Apply filters to expense list.
        
        Args:
            expenses: List of expenses to filter
            month: Filter by month (YYYY-MM format)
            category: Filter by category
            min_amount: Minimum amount filter
            max_amount: Maximum amount filter
            from_date: Start date filter
            to_date: End date filter
            
        Returns:
            Filtered list of expenses
        """
        filtered = expenses
        
        # Month filter
        if month:
            filtered = [exp for exp in filtered if exp.date.startswith(month)]
        
        # Date range filter
        if from_date:
            filtered = [exp for exp in filtered if exp.date >= from_date]
        if to_date:
            filtered = [exp for exp in filtered if exp.date <= to_date]
        
        # Category filter
        if category:
            category_lower = category.lower()
            filtered = [exp for exp in filtered if exp.category == category_lower]
        
        # Amount filters
        if min_amount is not None:
            filtered = [exp for exp in filtered if exp.amount >= min_amount]
        if max_amount is not None:
            filtered = [exp for exp in filtered if exp.amount <= max_amount]
        
        return filtered
