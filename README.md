# Python Contact Management System

A robust, console-based digital phonebook built with Python 3.10+ demonstrating dictionary data structures, nested key-value mappings, input validation, and persistent JSON storage. Developed as a comprehensive solution for Tech Internships practical assignments.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technologies & Core Concepts](#technologies--core-concepts)
4. [Python Version Requirements](#python-version-requirements)
5. [Project Folder Structure](#project-folder-structure)
6. [JSON Data Storage](#json-data-storage)
7. [Input Validation & Error Handling](#input-validation--error-handling)
8. [Setup and Execution Instructions](#setup-and-execution-instructions)
9. [Sample Console Output](#sample-console-output)
10. [Step-by-Step Testing Checklist](#step-by-step-testing-checklist)
11. [Git & GitHub Submission Guide](#git--github-submission-guide)
12. [Grading Criteria Alignment](#grading-criteria-alignment)

---

## 1. Project Overview

The **Contact Management System** is an interactive, menu-driven CLI (Command Line Interface) application designed to manage personal and business contacts. Users can add, search, view, update, and delete contacts, with changes automatically persisting to a `contacts.json` file.

The application ensures high data integrity by enforcing international phone number formatting, standard RFC email validation, non-empty text constraints, and case-insensitive uniqueness checks to prevent duplicate entries.

---

## 2. Key Features

- **Add Contact (Create)**: Accepts full name, phone number, email address, and physical address. Validates all inputs and prevents case-insensitive duplicate names.
- **Search Contact (Read)**: Case-insensitive and whitespace-tolerant search for any contact name. Displays full contact cards with phone, email, and address.
- **View All Contacts (Read)**: Formatted, indexed list of all records with summary metrics (total contact count) and graceful empty-state handling.
- **Update Contact (Update)**: Allows updating phone numbers and email addresses while preserving unmodified fields by pressing Enter. Re-validates updated values.
- **Delete Contact (Delete)**: Features safety confirmation (`y/n`) prior to removing any record to prevent accidental data loss.
- **Save & Exit**: Synchronizes memory state to `contacts.json` and cleanly exits the application.
- **Automatic Persistence**: Every successful addition, update, or deletion immediately updates the JSON storage file on disk.

---

## 3. Technologies & Core Concepts

- **Language**: Python 3.10+
- **Standard Library Modules**:
  - `json`: Object serialization (`json.dump()`) and deserialization (`json.load()`).
  - `re`: Regular expressions for pattern-based phone and email validation.
  - `pathlib.Path`: Robust, cross-platform path resolution independent of terminal working directories.
  - `sys`: Safe program exit and exception handling.
- **Data Structures**:
  - **Nested Dictionaries**: Primary in-memory data store where the contact's full name is the primary key and the contact's details are stored in an inner dictionary.

---

## 4. Python Version Requirements

- **Python Version**: Python 3.10 or higher (Tested and verified on Python 3.13)
- **Supported Platforms**: Windows, macOS, and Linux
- **External Dependencies**: None (100% pure Python standard library)

---

## 5. Project Folder Structure

```text
Contact-Management-System/
│
├── main.py          # Primary application source code (menu loop, validation, CRUD, JSON IO)
├── contacts.json    # JSON storage file containing persistent contact records
├── README.md        # Comprehensive project documentation and execution guide
└── .gitignore       # Git ignore rules for caches, virtual environments, and temporary files
```

---

## 6. JSON Data Storage

All contacts are persisted to `contacts.json` located in the root project directory. The file uses UTF-8 encoding and four-space indentation (`indent=4`) for readability.

### Example Contact Record

```json
{
    "John Carter": {
        "phone": "+1-555-018-9922",
        "email": "john.c@example.com",
        "address": "42 Silicon Way, Tech City"
    }
}
```

### Demonstration Contacts

The repository comes pre-populated with sample records (`John Carter`, `Sarah Connor`, `Elena Rostova`) to facilitate immediate demonstration of search, update, view, and delete operations. If `contacts.json` is deleted or missing, the application automatically handles its absence and initializes a clean dictionary without errors.

---

## 7. Input Validation & Error Handling

| Category | Validation Rule | Behavior on Failure |
| :--- | :--- | :--- |
| **Name** | Non-empty after trimming; case-insensitive duplicate check | Rejects entry with error message; aborts operation |
| **Phone** | International formats: optional leading `+`, digits, spaces, hyphens, and `()`; requires 7 to 15 digits (E.164 standard) | Rejects entry with format guidance |
| **Email** | Standard RFC pattern: `[username]@[domain].[ext]` using `re` | Rejects invalid address format |
| **Address** | Non-empty after trimming | Rejects blank address |
| **JSON Storage** | Handles missing file, empty file, corrupt syntax, and file permission errors | Notifies user with warning and safely defaults to `{}` |
| **Menu Input** | Choice must be within `1` to `6` | Displays friendly error without terminating program |
| **Deletion** | Requires explicit `y` or `yes` confirmation | Cancels deletion if confirmation is declined |

---

## 8. Setup and Execution Instructions

### Step 1: Open the Project in Visual Studio Code
1. Launch **Visual Studio Code**.
2. Go to **File** > **Open Folder...** and select the `Contact-Management-System` directory.
3. Open an integrated terminal in VS Code using the shortcut:
   - **Windows/Linux**: `Ctrl + ` `~`
   - **macOS**: `Cmd + ` `~`

### Step 2: Verify Python Installation
In the VS Code terminal, verify that Python 3.10+ is installed:

```bash
python --version
# or on macOS/Linux:
python3 --version
```

### Step 3: Run the Application
Execute `main.py` using standard Python:

```bash
# Windows
python main.py

# macOS / Linux
python3 main.py
```

---

## 9. Sample Console Output

### 1. Main Menu
```text
=== PYTHON CONTACT MANAGER ===
1. Add Contact
2. Search Contact
3. View All Contacts
4. Update Contact
5. Delete Contact
6. Save & Exit

Enter choice (1-6): 1
```

### 2. Adding a Contact
```text
--- ADD NEW CONTACT ---
Enter Name: Marcus Vance
Enter Phone: +1-555-432-8877
Enter Email: marcus.vance@innovate.org
Enter Address: 808 Innovation Blvd, Austin, TX

-> Contact 'Marcus Vance' saved to 'contacts.json' successfully!
```

### 3. Searching for a Contact
```text
--- SEARCH CONTACT ---
Enter name to search: john carter

[SEARCH MATCH FOUND]
-----------------------------------
Name    : John Carter
Phone   : +1-555-018-9922
Email   : john.c@example.com
Address : 42 Silicon Way, Tech City
-----------------------------------
```

### 4. Viewing All Contacts
```text
--- ALL CONTACTS ---
Total Contacts: 3

============================================================
#1 | John Carter
     Phone   : +1-555-018-9922
     Email   : john.c@example.com
     Address : 42 Silicon Way, Tech City
------------------------------------------------------------
#2 | Sarah Connor
     Phone   : +1-555-019-3344
     Email   : sarah.connor@cyberdyne.io
     Address : 100 Resistance Blvd, Los Angeles, CA
------------------------------------------------------------
#3 | Elena Rostova
     Phone   : +44 20 7946 0958
     Email   : elena.rostova@techglobal.org
     Address : 14 Kensington High St, London, UK
============================================================
```

### 5. Updating a Contact
```text
--- UPDATE CONTACT ---
Enter name of contact to update: John Carter

Updating details for: John Carter
(Press [Enter] without typing to keep existing details)
Enter new Phone [+1-555-018-9922]: +1-555-999-0011
Enter new Email [john.c@example.com]: 
Enter new Address [42 Silicon Way, Tech City]: 

-> Contact 'John Carter' updated and saved to 'contacts.json' successfully!
```

### 6. Deleting a Contact
```text
--- DELETE CONTACT ---
Enter name of contact to delete: Elena Rostova
Are you sure you want to permanently delete 'Elena Rostova'? (y/n): y

-> Contact 'Elena Rostova' deleted and 'contacts.json' updated successfully.
```

---

## 10. Step-by-Step Testing Checklist

| # | Test Scenario | Input / Action | Expected Result | Status |
| :---: | :--- | :--- | :--- | :---: |
| 1 | Add valid contact | Name, +1-555-123-4567, user@test.com, 123 Elm St | Contact added & saved | Passed |
| 2 | Add contact with invalid phone | Phone: `abc-123` | Error displayed, contact rejected | Passed |
| 3 | Add contact with invalid email | Email: `not-an-email` | Error displayed, contact rejected | Passed |
| 4 | Attempt duplicate name with different case | Name: `john carter` | Error: contact already exists | Passed |
| 5 | Search existing contact (case-insensitive) | Search: `sArAh CoNnOr` | Full contact details displayed | Passed |
| 6 | Search nonexistent contact | Search: `Unknown Person` | `[Not Found]` message displayed | Passed |
| 7 | View all contacts with data | Option `3` | Formatted list with total count | Passed |
| 8 | View all contacts when empty | Delete all records, then Option `3` | "Your phonebook is currently empty." | Passed |
| 9 | Update contact's phone and email | Enter new phone & email, blank address | Phone & email updated; address preserved | Passed |
| 10 | Update nonexistent contact | Name: `Nobody` | `[Not Found]` error displayed | Passed |
| 11 | Delete contact with confirmation | Confirm: `y` | Contact deleted, JSON file updated | Passed |
| 12 | Cancel contact deletion | Confirm: `n` | Deletion cancelled, record kept | Passed |
| 13 | Exit and restart persistence | Exit via `6`, restart `python main.py` | Data persists accurately across sessions | Passed |
| 14 | Start when `contacts.json` is missing | Delete `contacts.json`, run `main.py` | Starts gracefully with empty dict `{}` | Passed |
| 15 | Enter invalid menu option | Choice: `9` or `abc` | `[Invalid Input]` warning, loop continues | Passed |
| 16 | JSON validity after multiple operations | Perform Add, Update, Delete | `contacts.json` remains valid JSON | Passed |

---

## 11. Git & GitHub Submission Guide

Follow these commands to initialize git, commit files, and push to GitHub:

### 1. Initialize Local Git Repository
```bash
git init
git add .
git commit -m "feat: complete Python Contact Management System implementation"
```

### 2. Rename Default Branch to `main`
```bash
git branch -M main
```

### 3. Create a Remote Repository on GitHub
1. Log in to [GitHub](https://github.com).
2. Click the **+** icon in the upper right corner > **New repository**.
3. Set **Repository name** to: `Contact-Management-System`
4. Set description to:
   `A Python-based Contact Management System using nested dictionaries and JSON file storage, featuring contact CRUD operations, search, validation, and persistent data management.`
5. Leave it **Public** and **do not** check "Initialize this repository with a README".
6. Click **Create repository**.

### 4. Link Remote and Push
```bash
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/Contact-Management-System.git
git push -u origin main
```

### Submission URL Format
Paste the resulting public repository link into your Tech Internships submission form:
```text
https://github.com/<YOUR_GITHUB_USERNAME>/Contact-Management-System
```

---

## 12. Grading Criteria Alignment

- **Dictionary Operations (40%)**:
  - Implements nested dictionary structures where the name is the outer key and attributes (`phone`, `email`, `address`) form the inner dictionary.
  - CRUD operations (Create, Read, Update, Delete) are cleanly isolated in functions.
- **JSON File Storage (30%)**:
  - Functions `save_contacts()` and `load_contacts()` ensure full data persistence.
  - Automatic persistence after every state-modifying action.
  - Uses UTF-8 encoding and human-readable indentation.
- **Search Speed & Strategy (30%)**:
  - Uses direct key indexing and case-normalized matching via `find_contact_key()`.
  - O(N) case-insensitive search with immediate exit upon match; preserves original key formatting.
