"""
Command-line interface for expense tracker.
"""

import argparse
import logging
import sys
from typing import Optional
from tracker.service import ExpenseService
from tracker.storage import ExpenseStorage
from tracker.logger import setup_logging

logger = logging.getLogger(__name__)


def cmd_add(args, service: ExpenseService):
    """Handle add command."""
    try:
        logger.info(f"Command: add - category={args.category}, amount={args.amount}")
        
        expense = service.add_expense(
            date=args.date,
            category=args.category,
            amount=args.amount,
            note=args.note,
            currency=args.currency
        )
        
        print(f"Added: {expense}")
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def cmd_list(args, service: ExpenseService):
    """Handle list command."""
    try:
        logger.info(f"Command: list - filters: month={args.month}, category={args.category}")
        
        expenses = service.list_expenses(
            month=args.month,
            category=args.category,
            min_amount=args.min,
            max_amount=args.max,
            sort_by=args.sort,
            descending=args.desc,
            limit=args.limit
        )
        
        if not expenses:
            print("No expenses found")
            return
        
        print(f"\nFound {len(expenses)} expense(s):\n")
        print("-" * 80)
        
        for expense in expenses:
            print(expense)
        
        print("-" * 80)
        print(f"Total: {len(expenses)} expense(s)")
        
    except Exception as e:
        logger.error(f"Error listing expenses: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def cmd_summary(args, service: ExpenseService):
    """Handle summary command."""
    try:
        logger.info(f"Command: summary - filters: month={args.month}, category={args.category}")
        
        summary = service.summary(
            month=args.month,
            category=args.category,
            from_date=getattr(args, 'from', None),
            to_date=args.to
        )
        
        if summary["count"] == 0:
            print("No expenses found")
            return
        
        print("\n" + "=" * 60)
        print("EXPENSE SUMMARY")
        print("=" * 60)
        
        # Display filters if any
        if args.month:
            print(f"Period: {args.month}")
        elif getattr(args, 'from', None) or args.to:
            from_date = getattr(args, 'from', None) or "start"
            to_date = args.to or "end"
            print(f"Period: {from_date} to {to_date}")
        
        if args.category:
            print(f"Category: {args.category}")
        
        print("-" * 60)
        
        # Category breakdown
        print("\nBreakdown by Category:")
        print("-" * 60)
        
        # Sort categories by amount (descending)
        sorted_categories = sorted(
            summary["totals_by_category"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for category, total in sorted_categories:
            percentage = (total / summary["grand_total"] * 100) if summary["grand_total"] > 0 else 0
            print(f"{category:20s}: {total:10.2f} {summary['currency']} ({percentage:5.1f}%)")
        
        print("-" * 60)
        print(f"{'GRAND TOTAL':20s}: {summary['grand_total']:10.2f} {summary['currency']}")
        print(f"{'Total Expenses':20s}: {summary['count']}")
        print("=" * 60 + "\n")
        
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def cmd_delete(args, service: ExpenseService):
    """Handle delete command."""
    try:
        logger.info(f"Command: delete - id={args.id}")
        
        result = service.delete_expense(args.id)
        
        if result:
            print(f"Deleted: {args.id}")
        else:
            print(f"Error: Expense {args.id} not found")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error deleting expense: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def cmd_edit(args, service: ExpenseService):
    """Handle edit command."""
    try:
        logger.info(f"Command: edit - id={args.id}")
        
        updates = {}
        if args.amount is not None:
            updates["amount"] = args.amount
        if args.note is not None:
            updates["note"] = args.note
        if args.category is not None:
            updates["category"] = args.category
        if args.date is not None:
            updates["date"] = args.date
        
        if not updates:
            print("Error: No fields to update")
            sys.exit(1)
        
        result = service.edit_expense(args.id, **updates)
        
        if result:
            print(f"Updated: {result}")
        else:
            print(f"Error: Expense {args.id} not found")
            sys.exit(1)
            
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error editing expense: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description="Expense Tracker CLI",
        prog="python -m tracker"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--date", help="Date in YYYY-MM-DD format (default: today)")
    add_parser.add_argument("--category", required=True, help="Expense category (e.g., food, transport)")
    add_parser.add_argument("--amount", type=float, required=True, help="Expense amount (must be > 0)")
    add_parser.add_argument("--note", default="", help="Optional note")
    add_parser.add_argument("--currency", default="BDT", help="Currency code (default: BDT)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List expenses with filters")
    list_parser.add_argument("--month", help="Filter by month (YYYY-MM)")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--min", type=float, help="Minimum amount")
    list_parser.add_argument("--max", type=float, help="Maximum amount")
    list_parser.add_argument("--sort", default="date", choices=["date", "amount", "category"], 
                            help="Sort by field (default: date)")
    list_parser.add_argument("--desc", action="store_true", help="Sort in descending order")
    list_parser.add_argument("--limit", type=int, help="Limit number of results")
    
    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show expense summary")
    summary_parser.add_argument("--month", help="Filter by month (YYYY-MM)")
    summary_parser.add_argument("--category", help="Filter by category")
    summary_parser.add_argument("--from", dest="from", help="Start date (YYYY-MM-DD)")
    summary_parser.add_argument("--to", help="End date (YYYY-MM-DD)")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("--id", required=True, help="Expense ID to delete")
    
    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit an expense")
    edit_parser.add_argument("--id", required=True, help="Expense ID to edit")
    edit_parser.add_argument("--amount", type=float, help="New amount")
    edit_parser.add_argument("--note", help="New note")
    edit_parser.add_argument("--category", help="New category")
    edit_parser.add_argument("--date", help="New date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize service
    storage = ExpenseStorage()
    service = ExpenseService(storage)
    
    # Route to appropriate command handler
    if args.command == "add":
        cmd_add(args, service)
    elif args.command == "list":
        cmd_list(args, service)
    elif args.command == "summary":
        cmd_summary(args, service)
    elif args.command == "delete":
        cmd_delete(args, service)
    elif args.command == "edit":
        cmd_edit(args, service)

