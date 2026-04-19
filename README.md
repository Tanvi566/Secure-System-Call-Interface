# 🛡️ Secure System Call Interface

A modern GUI-based terminal emulator with user authentication, role-based access control, and sandboxed file operations. Built as a Linux-like system shell interface with an elegant dark-themed desktop application.

## 🌟 Features

### Authentication & Security
- **User Registration & Login** - Create new user accounts with username and password
- **Login Attempts Tracking** - System locks after 5 failed login attempts for security
- **Role-Based Access Control** - Two access levels:
  - **SUPERUSER (admin)** - Full system access including user management and file deletion
  - **USER** - Limited access to file operations and directory navigation
- **Session Management** - Auto-logout after 2 minutes of inactivity
- **Action Logging** - All user actions are logged with timestamps

### File Operations
- **ls** - List directory contents with file permissions
- **touch** - Create new empty files
- **cat** - Read and display file contents
- **echo** - Write data to files
- **mv** - Move or rename files and directories
- **cp** - Copy files
- **rm** - Delete files (Admin only)
- **rmdir** - Delete directories (Admin only)
- **grep** - Search for text patterns within files
- **wc** - Count lines, words, and characters in files
- **find** - Search for files by name across the directory tree

### Directory Navigation
- **pwd** - Print working directory path
- **cd** - Change directory
- **cd ..** - Navigate to parent directory
- **mkdir** - Create new directories (auto-enters created directory)
- **tree** - Display complete directory structure in tree format

### System & Admin Commands
- **useradd** - Create new user accounts (Admin only)
- **userdel** - Delete user accounts (Admin only) - Cannot delete primary admin
- **users** - List all registered users (Admin only)
- **passwd** - Change current user password
- **whoami** - Display current logged-in username
- **date** - Show current date and time
- **uname** - Display system information
- **history** - Show command execution history
- **tail** - View system activity logs
- **clear** - Clear terminal screen
- **help** - Display all available commands with descriptions

### UI/UX Features
- **Dark Modern Theme** - Professional dark interface with color-coded output
- **Live Terminal Emulation** - Real-time command prompt with history support
- **Session Timer** - Live display of session duration
- **Command Sidebar** - Quick-access buttons for all commands
- **Input Dialogs** - Context-aware input windows for command parameters
- **Syntax Highlighting** - Color-coded output for different message types:
  - 🟡 System messages (Yellow)
  - 🔵 Commands (Cyan)
  - 🟢 Success messages (Green)
  - 🔴 Error messages (Red)
  - 🟣 Highlighted text search results (Purple)
- **File Viewer** - Dedicated window for viewing file contents
- **Log Viewer** - Scrollable window to review system activity logs

## 🔒 Security Features

### Sandbox Environment
- **Path Restriction** - All file operations are restricted to the `project_files` directory
- **Sandbox Escape Prevention** - Blocks attempts to navigate above the root project directory
- **Safe Path Validation** - Every file operation validates paths to prevent unauthorized access

### Access Control
- **Permission System** - Different commands have different privilege levels
  - File deletion (rm, rmdir) - Admin only
  - User management (useradd, userdel, users) - Admin only
  - Log clearing - Admin only
  - Password change - All users
  - File operations - All users (within sandbox)

### Activity Monitoring
- **Comprehensive Logging** - Every action is logged with:
  - Timestamp
  - Username
  - Action performed
- **Session Tracking** - Session start time and duration monitoring
- **Inactivity Detection** - Automatic session termination after 120 seconds of no activity

## 🛠️ Technology Stack

### Frontend Framework
- **CustomTkinter** - Modern Python GUI toolkit with dark mode support
- **Tkinter** - Python's standard GUI library (base for CustomTkinter)

### Backend
- **Python 3** - Core programming language
- **File I/O** - Text-based user and log storage
- **OS Module** - File system operations and path management
- **Shutil Module** - Advanced file operations (copy, tree deletion)
- **Stat Module** - File permission modification
- **Datetime Module** - Timestamp and time tracking

### Data Storage
- **users.txt** - Plain text file storing usernames and passwords (username,password format)
- **logs.txt** - Plain text file keeping activity logs
- **project_files/** - Sandboxed directory for user files

## 🚀 Getting Started

### Prerequisites
```bash
pip install customtkinter
```

### Running the Application
```bash
python main.py
```

### Initial Setup
1. On first launch, register an admin account using username "admin"
2. The system creates:
   - `users.txt` - User credentials file
   - `logs.txt` - Activity log file
   - `project_files/` - Sandbox directory
3. Login with your credentials
4. All subsequent users should be created via the `useradd` command (Admin only)

## 📋 Command Examples

### File Operations
```
touch myfile.txt          # Create new file
cat myfile.txt            # Read file
echo > myfile.txt         # Write to file with multi-line input
cp myfile.txt backup.txt  # Copy file
mv myfile.txt renamed.txt # Rename file
rm myfile.txt             # Delete file (admin only)
```

### Directory Operations
```
mkdir newfolder           # Create new directory
cd newfolder              # Enter directory
pwd                        # Show current path
cd ..                     # Go back one level
ls                        # List directory contents
tree                      # Show directory structure
find myfile.txt           # Search for file anywhere
```

### User Management (Admin Only)
```
useradd john              # Create new user
userdel john              # Delete user
users                     # List all users
```

### System Commands
```
whoami                    # Show current user
date                      # Show current time
history                   # Show command history
tail                      # View system logs
passwd                    # Change password
help                      # Display all commands
```

## 🏗️ Project Structure

```
Secure-System-Call-Interface/
├── main.py                 # Main application file
├── README.md              # This file
├── users.txt              # User credentials (created at runtime)
├── logs.txt               # Activity logs (created at runtime)
└── project_files/         # Sandboxed directory for user files
    └── (user-created files and folders)
```

## 🔐 Security Considerations

1. **Password Storage** - Passwords are stored in plain text (not for production use)
2. **Sandbox Isolation** - Users can only access files within the `project_files` directory
3. **Admin Protection** - Primary admin account cannot be deleted
4. **Session Security** - Automatic logout on inactivity
5. **Login Protection** - Account lock after multiple failed attempts
6. **Permission Enforcement** - Critical operations require admin privileges

## 🎨 UI Components

- **Top Navbar** - Shows SecureSys title, session timer, user info, and logout button
- **Left Sidebar** - Quick-access command buttons organized by function
- **Terminal Area** - Main display showing command prompts and outputs
- **Command Input Bar** - Live command prompt with dynamic path display
- **Modal Dialogs** - Input windows for command parameters and file viewing

## 📝 Logging Format

System logs follow this format:
```
2026-03-31 14:23:45.123456 - username: action description
```

Examples:
```
2026-03-31 14:23:45.123456 - admin: Created new user 'john'
2026-03-31 14:23:50.234567 - john: Executed 'ls'
2026-03-31 14:24:15.345678 - john: Created file test.txt
```

## ⚙️ Configuration

### Timeout Settings
- **Idle Timeout** - 120 seconds (2 minutes).
- **Login Attempts** - 5 attempts before system lock.

### Theme
- **Appearance** - Dark mode.
- **Color Scheme** - Blue primary theme.
- **Font** - Consolas for terminal, Roboto for UI.

## 🐛 Limitations & Notes

1. **Single-User Sessions** - Only one user can be logged in at a time.
2. **Plain Text Storage** - User data stored in plain text files (not encrypted).
3. **No Network Features** - Operates locally only.
4. **No Command Chaining** - Commands must be executed individually.
5. **No Script Execution** - Cannot execute bash scripts or system binaries.

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

**Built with Python, CustomTkinter, and a passion for secure system design** 🚀
