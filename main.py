"""
=============================================================================
Contact Management System
=============================================================================
Description : A console-based digital phonebook built in Python 3.10+.
              Features CRUD operations, nested dictionary storage,
              phone & email validation, case-insensitive search, and
              persistent JSON data storage.
Author      : Senior Python Mentor & Developer (Tech Internships Assignment)
=============================================================================
"""

import json
import re
import sys
from pathlib import Path

# Set the path to contacts.json in the same directory as main.py
STORAGE_FILE: Path = Path(__file__).resolve().parent / "contacts.json"


# ---------------------------------------------------------------------------
# Validation Helper Functions
# ---------------------------------------------------------------------------

def validate_phone(phone: str) -> bool:
    """
    Validates a phone number supporting international formats.
    
    Accepts leading '+', digits, spaces, hyphens, and parentheses.
    Ensures that the total count of digits is between 7 and 15 (E.164 standard).
    
    Args:
        phone (str): The phone number string to validate.
        
    Returns:
        bool: True if the phone number is valid, False otherwise.
    """
    cleaned = phone.strip()
    if not cleaned:
        return False
        
    # Pattern allows optional '+' followed by digits, spaces, hyphens, and parentheses
    allowed_pattern = r"^\+?[\d\s\-()]{7,25}$"
    if not re.match(allowed_pattern, cleaned):
        return False
        
    # Extract only digit characters to check realistic length
    digits = re.sub(r"\D", "", cleaned)
    return 7 <= len(digits) <= 15


def validate_email(email: str) -> bool:
    """
    Validates an email address using standard RFC-compliant regex pattern.
    
    Args:
        email (str): The email string to validate.
        
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    cleaned = email.strip()
    if not cleaned:
        return False
        
    # Standard email pattern: username@domain.extension
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(email_pattern, cleaned))


# ---------------------------------------------------------------------------
# JSON Persistence Functions
# ---------------------------------------------------------------------------

def load_contacts(filepath: Path) -> dict:
    """
    Loads contacts from a JSON file.
    
    Handles missing file, empty file, invalid JSON syntax, and OS errors
    gracefully without crashing the application.
    
    Args:
        filepath (Path): Path to the JSON storage file.
        
    Returns:
        dict: The dictionary of loaded contacts or an empty dictionary.
    """
    if not filepath.exists():
        # File doesn't exist yet; initialize an empty contact book
        return {}
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                # File exists but is empty
                return {}
            data = json.loads(content)
            if isinstance(data, dict):
                return data
            else:
                print(f"\n[Warning] File '{filepath.name}' has unexpected data structure. Initializing empty.")
                return {}
    except json.JSONDecodeError:
        print(f"\n[Warning] '{filepath.name}' contains corrupted or invalid JSON. Initializing empty.")
        return {}
    except OSError as e:
        print(f"\n[Error] Unable to read '{filepath.name}': {e}")
        return {}


def save_contacts(filepath: Path, contacts: dict) -> bool:
    """
    Saves the entire contacts dictionary to a JSON file with formatting.
    
    Uses UTF-8 encoding and indent=4 for human readability.
    
    Args:
        filepath (Path): Path to the JSON storage file.
        contacts (dict): The contacts dictionary to persist.
        
    Returns:
        bool: True if saving succeeded, False otherwise.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=4, ensure_ascii=False)
        return True
    except OSError as e:
        print(f"\n[Error] Failed to save contacts to '{filepath.name}': {e}")
        return False


# ---------------------------------------------------------------------------
# Search and Lookup Strategy
# ---------------------------------------------------------------------------

def find_contact_key(contacts: dict, search_name: str) -> str | None:
    """
    Searches for a contact by full name, ignoring letter case and extra whitespace.
    
    Returns the exact key as stored in the dictionary, allowing case-insensitive
    lookups while preserving original casing.
    
    Args:
        contacts (dict): The contacts dictionary.
        search_name (str): The search query name.
        
    Returns:
        str | None: The actual dictionary key if found, None otherwise.
    """
    normalized_query = search_name.strip().lower()
    if not normalized_query:
        return None
        
    for key in contacts:
        if key.strip().lower() == normalized_query:
            return key
            
    return None


# ---------------------------------------------------------------------------
# CRUD Feature Functions
# ---------------------------------------------------------------------------

def add_contact(contacts: dict) -> None:
    """
    Feature 1: Adds a new contact with full validation.
    
    Prompts for Name, Phone, Email, and Address. Rejects empty fields,
    invalid phone/email formats, and case-insensitive duplicates.
    Saves immediately to storage file upon success.
    """
    print("\n--- ADD NEW CONTACT ---")
    
    # 1. Contact Name
    name = input("Enter Name: ").strip()
    if not name:
        print("[Error] Contact name cannot be empty!")
        return
        
    # Check for duplicate name (case-insensitive)
    existing_key = find_contact_key(contacts, name)
    if existing_key:
        print(f"[Error] Contact '{existing_key}' already exists in your phonebook!")
        return
        
    # 2. Phone Number
    phone = input("Enter Phone: ").strip()
    if not phone:
        print("[Error] Phone number cannot be empty!")
        return
    if not validate_phone(phone):
        print("[Error] Invalid phone number! Please enter a valid international or local number (e.g. +1-555-018-9922).")
        return
        
    # 3. Email Address
    email = input("Enter Email: ").strip()
    if not email:
        print("[Error] Email address cannot be empty!")
        return
    if not validate_email(email):
        print("[Error] Invalid email address format! (e.g. user@example.com)")
        return
        
    # 4. Physical / Residential Address
    address = input("Enter Address: ").strip()
    if not address:
        print("[Error] Address cannot be empty!")
        return
        
    # Store contact in nested dictionary structure
    contacts[name] = {
        "phone": phone,
        "email": email,
        "address": address
    }
    
    # Automatically persist changes
    if save_contacts(STORAGE_FILE, contacts):
        print(f"\n-> Contact '{name}' saved to '{STORAGE_FILE.name}' successfully!")


def search_contact(contacts: dict) -> None:
    """
    Feature 2: Searches for an existing contact by name (case-insensitive).
    
    Displays Name, Phone, Email, and Address when found.
    Displays a friendly message when not found.
    """
    print("\n--- SEARCH CONTACT ---")
    query = input("Enter name to search: ").strip()
    if not query:
        print("[Error] Search query cannot be empty!")
        return
        
    match_key = find_contact_key(contacts, query)
    if match_key:
        details = contacts[match_key]
        print("\n[SEARCH MATCH FOUND]")
        print("-" * 35)
        print(f"Name    : {match_key}")
        print(f"Phone   : {details.get('phone', 'N/A')}")
        print(f"Email   : {details.get('email', 'N/A')}")
        print(f"Address : {details.get('address', 'N/A')}")
        print("-" * 35)
    else:
        print(f"\n[Not Found] No contact found matching '{query}'.")


def view_all_contacts(contacts: dict) -> None:
    """
    Feature 3: Displays all saved contacts in a clean, formatted layout.
    
    Displays the total contact count and handles empty phonebook gracefully.
    """
    print("\n--- ALL CONTACTS ---")
    total = len(contacts)
    
    if total == 0:
        print("Your phonebook is currently empty. No contacts to display.")
        return
        
    print(f"Total Contacts: {total}\n")
    print("=" * 60)
    for idx, (name, details) in enumerate(contacts.items(), start=1):
        print(f"#{idx} | {name}")
        print(f"     Phone   : {details.get('phone', 'N/A')}")
        print(f"     Email   : {details.get('email', 'N/A')}")
        print(f"     Address : {details.get('address', 'N/A')}")
        if idx < total:
            print("-" * 60)
    print("=" * 60)


def update_contact(contacts: dict) -> None:
    """
    Feature 4: Updates an existing contact's phone and email.
    
    Supports case-insensitive contact selection. Allows the user to keep
    existing values by pressing Enter without typing new values.
    Validates any newly provided phone or email before saving.
    """
    print("\n--- UPDATE CONTACT ---")
    search_name = input("Enter name of contact to update: ").strip()
    if not search_name:
        print("[Error] Search name cannot be empty!")
        return
        
    match_key = find_contact_key(contacts, search_name)
    if not match_key:
        print(f"[Not Found] Contact '{search_name}' does not exist.")
        return
        
    current = contacts[match_key]
    print(f"\nUpdating details for: {match_key}")
    print("(Press [Enter] without typing to keep existing details)")
    
    # 1. Update Phone
    new_phone = input(f"Enter new Phone [{current['phone']}]: ").strip()
    if new_phone:
        if not validate_phone(new_phone):
            print("[Error] Invalid phone number format! Update aborted.")
            return
        updated_phone = new_phone
    else:
        updated_phone = current["phone"]
        
    # 2. Update Email
    new_email = input(f"Enter new Email [{current['email']}]: ").strip()
    if new_email:
        if not validate_email(new_email):
            print("[Error] Invalid email address format! Update aborted.")
            return
        updated_email = new_email
    else:
        updated_email = current["email"]
        
    # 3. Update Address (optional convenience)
    new_address = input(f"Enter new Address [{current['address']}]: ").strip()
    updated_address = new_address if new_address else current["address"]
    
    # Apply updates
    contacts[match_key] = {
        "phone": updated_phone,
        "email": updated_email,
        "address": updated_address
    }
    
    if save_contacts(STORAGE_FILE, contacts):
        print(f"\n-> Contact '{match_key}' updated and saved to '{STORAGE_FILE.name}' successfully!")


def delete_contact(contacts: dict) -> None:
    """
    Feature 5: Deletes a contact by name with mandatory user confirmation.
    
    Prompts for confirmation ('y'/'yes'). Upon confirmation, removes the
    contact and updates the JSON file.
    """
    print("\n--- DELETE CONTACT ---")
    search_name = input("Enter name of contact to delete: ").strip()
    if not search_name:
        print("[Error] Contact name cannot be empty!")
        return
        
    match_key = find_contact_key(contacts, search_name)
    if not match_key:
        print(f"[Not Found] Contact '{search_name}' does not exist.")
        return
        
    # Mandatory confirmation prompt
    confirm = input(f"Are you sure you want to permanently delete '{match_key}'? (y/n): ").strip().lower()
    if confirm in ("y", "yes"):
        del contacts[match_key]
        if save_contacts(STORAGE_FILE, contacts):
            print(f"\n-> Contact '{match_key}' deleted and '{STORAGE_FILE.name}' updated successfully.")
    else:
        print("\n-> Deletion cancelled. Contact was not deleted.")


def save_and_exit(contacts: dict) -> None:
    """
    Feature 6: Persists all current contacts and exits cleanly.
    """
    print("\nSaving contacts before exit...")
    save_contacts(STORAGE_FILE, contacts)
    print("Contacts successfully saved to 'contacts.json'. Exiting program. Goodbye!\n")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Main Menu & Application Entry Point
# ---------------------------------------------------------------------------

def display_menu() -> None:
    """Displays the standardized application console menu."""
    print("\n=== PYTHON CONTACT MANAGER ===")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. View All Contacts")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Save & Exit")


def main() -> None:
    """
    Application entry point. Initializes contact data from JSON,
    and runs the interactive command loop.
    """
    # Load existing contacts from storage file
    contacts = load_contacts(STORAGE_FILE)
    
    while True:
        display_menu()
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contact(contacts)
        elif choice == "3":
            view_all_contacts(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            save_and_exit(contacts)
        else:
            print(f"\n[Invalid Input] '{choice}' is not a valid choice. Please select an option from 1 to 6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Interrupted] Application terminated by user. Goodbye!")
        sys.exit(0)
