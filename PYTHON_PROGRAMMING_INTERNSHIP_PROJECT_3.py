import os
import datetime
import json
from tabulate import tabulate
import matplotlib.pyplot as plt
from collections import defaultdict

class ExpenseTracker:
    def __init__(self):
        """Initialize the Expense Tracker application."""
        self.expenses = []
        self.categories = ["Food", "Transportation", "Entertainment", "Housing", "Utilities", "Shopping", "Health", "Education", "Other"]
        self.data_file = "expenses.json"
        self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from the JSON file if available."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    self.expenses = json.load(file)
                print("Expenses loaded successfully!")
        except Exception as e:
            print(f"Error loading expenses: {e}")
            self.expenses = []

    def save_expenses(self):
        """Save expenses to the JSON file."""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.expenses, file, indent=4)
            print("Expenses saved successfully!")
        except Exception as e:
            print(f"Error saving expenses: {e}")

    def add_expense(self):
        """Add a new expense."""
        print("\n=== Add New Expense ===")
        
        # Get date
        while True:
            date_input = input("Date (YYYY-MM-DD, leave empty for today): ")
            if not date_input:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                break
            try:
                # Validate date format
                datetime.datetime.strptime(date_input, "%Y-%m-%d")
                date = date_input
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        # Get amount
        while True:
            amount_input = input("Amount spent: ")
            try:
                amount = float(amount_input)
                if amount < 0:
                    print("Amount cannot be negative.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        # Get description
        description = input("Description: ")
        
        # Choose category
        print("\nCategories:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")
        
        while True:
            category_input = input("Select category number: ")
            try:
                category_index = int(category_input) - 1
                if 0 <= category_index < len(self.categories):
                    category = self.categories[category_index]
                    break
                else:
                    print("Invalid category number.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Create expense entry
        expense = {
            "date": date,
            "amount": amount,
            "description": description,
            "category": category
        }
        
        self.expenses.append(expense)
        self.save_expenses()
        print("Expense added successfully!")

    def view_expenses(self):
        """View all expenses."""
        if not self.expenses:
            print("\nNo expenses found.")
            return
        
        print("\n=== All Expenses ===")
        table_data = []
        
        for i, expense in enumerate(self.expenses, 1):
            table_data.append([
                i,
                expense["date"],
                expense["category"],
                f"${expense['amount']:.2f}",
                expense["description"]
            ])
        
        headers = ["#", "Date", "Category", "Amount", "Description"]
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))

    def delete_expense(self):
        """Delete an expense."""
        self.view_expenses()
        
        if not self.expenses:
            return
        
        while True:
            index_input = input("\nEnter the number of the expense to delete (0 to cancel): ")
            try:
                index = int(index_input)
                if index == 0:
                    print("Deletion cancelled.")
                    return
                if 1 <= index <= len(self.expenses):
                    expense = self.expenses[index - 1]
                    print(f"Deleting: {expense['date']} - {expense['category']} - ${expense['amount']:.2f} - {expense['description']}")
                    confirm = input("Are you sure? (y/n): ").lower()
                    if confirm == 'y':
                        self.expenses.pop(index - 1)
                        self.save_expenses()
                        print("Expense deleted successfully!")
                    else:
                        print("Deletion cancelled.")
                    return
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a valid number.")

    def monthly_summary(self):
        """Show summary of expenses for a specific month."""
        if not self.expenses:
            print("\nNo expenses found.")
            return
        
        # Get user input for month and year
        while True:
            year_month = input("\nEnter month and year (YYYY-MM, leave empty for current month): ")
            if not year_month:
                year_month = datetime.datetime.now().strftime("%Y-%m")
                break
            try:
                datetime.datetime.strptime(year_month, "%Y-%m")
                break
            except ValueError:
                print("Invalid format. Please use YYYY-MM.")
        
        # Filter expenses for the specified month
        month_expenses = [expense for expense in self.expenses if expense["date"].startswith(year_month)]
        
        if not month_expenses:
            print(f"No expenses found for {year_month}.")
            return
        
        # Calculate statistics
        total_spent = sum(expense["amount"] for expense in month_expenses)
        category_totals = defaultdict(float)
        
        for expense in month_expenses:
            category_totals[expense["category"]] += expense["amount"]
        
        # Display summary
        print(f"\n=== Monthly Summary for {year_month} ===")
        print(f"Total expenses: ${total_spent:.2f}")
        print(f"Number of transactions: {len(month_expenses)}")
        
        print("\nCategory breakdown:")
        table_data = []
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_spent) * 100
            table_data.append([category, f"${amount:.2f}", f"{percentage:.2f}%"])
        
        headers = ["Category", "Amount", "Percentage"]
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))
        
        # Ask if user wants to see a pie chart
        show_chart = input("\nDo you want to see a pie chart visualization? (y/n): ").lower()
        if show_chart == 'y':
            self.show_pie_chart(category_totals, year_month)

    def show_pie_chart(self, category_totals, period):
        """Display a pie chart of expenses by category."""
        try:
            labels = list(category_totals.keys())
            sizes = list(category_totals.values())
            
            plt.figure(figsize=(10, 7))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title(f'Expenses by Category for {period}')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error displaying chart: {e}")
            print("You may need to install matplotlib using: pip install matplotlib")

    def category_analysis(self):
        """Show analysis of expenses by category."""
        if not self.expenses:
            print("\nNo expenses found.")
            return
        
        # Calculate statistics
        category_totals = defaultdict(float)
        
        for expense in self.expenses:
            category_totals[expense["category"]] += expense["amount"]
        
        total_spent = sum(category_totals.values())
        
        # Display summary
        print("\n=== Category Analysis (All Time) ===")
        print(f"Total expenses: ${total_spent:.2f}")
        
        table_data = []
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_spent) * 100
            table_data.append([category, f"${amount:.2f}", f"{percentage:.2f}%"])
        
        headers = ["Category", "Amount", "Percentage"]
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))
        
        # Ask if user wants to see a pie chart
        show_chart = input("\nDo you want to see a pie chart visualization? (y/n): ").lower()
        if show_chart == 'y':
            self.show_pie_chart(category_totals, "All Time")

    def edit_expense(self):
        """Edit an existing expense."""
        self.view_expenses()
        
        if not self.expenses:
            return
        
        while True:
            index_input = input("\nEnter the number of the expense to edit (0 to cancel): ")
            try:
                index = int(index_input)
                if index == 0:
                    print("Edit cancelled.")
                    return
                if 1 <= index <= len(self.expenses):
                    expense = self.expenses[index - 1]
                    print(f"\nEditing: {expense['date']} - {expense['category']} - ${expense['amount']:.2f} - {expense['description']}")
                    
                    # Get new values (empty input means keep the old value)
                    while True:
                        date_input = input(f"Date ({expense['date']}): ")
                        if not date_input:
                            date = expense['date']
                            break
                        try:
                            datetime.datetime.strptime(date_input, "%Y-%m-%d")
                            date = date_input
                            break
                        except ValueError:
                            print("Invalid date format. Please use YYYY-MM-DD.")
                    
                    while True:
                        amount_input = input(f"Amount (${expense['amount']:.2f}): ")
                        if not amount_input:
                            amount = expense['amount']
                            break
                        try:
                            amount = float(amount_input)
                            if amount < 0:
                                print("Amount cannot be negative.")
                                continue
                            break
                        except ValueError:
                            print("Invalid amount. Please enter a number.")
                    
                    description_input = input(f"Description ({expense['description']}): ")
                    description = description_input if description_input else expense['description']
                    
                    print("\nCategories:")
                    for i, category in enumerate(self.categories, 1):
                        print(f"{i}. {category}")
                    
                    while True:
                        category_input = input(f"Select category ({expense['category']}, 0 to keep current): ")
                        if not category_input or category_input == '0':
                            category = expense['category']
                            break
                        try:
                            category_index = int(category_input) - 1
                            if 0 <= category_index < len(self.categories):
                                category = self.categories[category_index]
                                break
                            else:
                                print("Invalid category number.")
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    # Update expense
                    self.expenses[index - 1] = {
                        "date": date,
                        "amount": amount,
                        "description": description,
                        "category": category
                    }
                    
                    self.save_expenses()
                    print("Expense updated successfully!")
                    return
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a valid number.")

    def run(self):
        """Run the expense tracker application."""
        while True:
            print("\n=== Expense Tracker Menu ===")
            print("1. Add Expense")
            print("2. View All Expenses")
            print("3. Edit Expense")
            print("4. Delete Expense")
            print("5. Monthly Summary")
            print("6. Category Analysis")
            print("0. Exit")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.edit_expense()
            elif choice == '4':
                self.delete_expense()
            elif choice == '5':
                self.monthly_summary()
            elif choice == '6':
                self.category_analysis()
            elif choice == '0':
                print("Thank you for using the Expense Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("=== Welcome to Expense Tracker ===")
    tracker = ExpenseTracker()
    tracker.run()