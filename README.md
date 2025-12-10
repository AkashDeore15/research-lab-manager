# 🔬 Research Lab Manager

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-12%2B-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

A comprehensive database application for managing university research laboratory operations. This system facilitates tracking of lab members, research projects, equipment usage, publications, and funding grants.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation Guide](#-installation-guide)
  - [Windows](#windows)
  - [Windows with WSL (Ubuntu)](#windows-with-wsl-ubuntu)
  - [macOS](#macos)
  - [Linux (Ubuntu/Debian)](#linux-ubuntudebian)
- [Database Setup](#-database-setup)
- [Running the Application](#-running-the-application)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Application Features](#-application-features)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 1. Project and Member Management
- ✅ Query, add, update, and remove members and projects
- ✅ Display detailed status of any project
- ✅ Show members who have worked on projects funded by a given grant
- ✅ Show mentorship relations among members on the same project

### 2. Equipment Usage Tracking
- ✅ Query, add, update, and remove equipment and usage records
- ✅ Show real-time status of equipment
- ✅ Track current users and their associated projects
- ✅ Enforce maximum 3 simultaneous users per equipment

### 3. Grant and Publication Reporting
- ✅ Identify member(s) with the highest number of publications
- ✅ Calculate average student publications per major
- ✅ Find funded projects active during a specific period
- ✅ Find top 3 most prolific members by grant

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.8+ |
| **Database** | PostgreSQL 12+ |
| **DB Adapter** | psycopg2 |
| **CLI Formatting** | tabulate |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.8 or higher
- **PostgreSQL** 12 or higher
- **pip** (Python package manager)
- **Git** (for cloning the repository)

---

## 🚀 Installation Guide

### Windows

#### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/windows/)
2. Run the installer
3. ⚠️ **Important:** Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### Step 2: Install PostgreSQL

1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer
3. During installation:
   - Set a password for the `postgres` user (remember this!)
   - Keep the default port `5432`
   - Complete the installation
4. Add PostgreSQL to PATH:
   - Open System Properties → Environment Variables
   - Add `C:\Program Files\PostgreSQL\15\bin` to PATH (adjust version number)
5. Verify installation:
   ```cmd
   psql --version
   ```

#### Step 3: Clone and Setup Project

```cmd
# Clone the repository
git clone https://github.com/AkashDeore15/research-lab-manager.git
cd research-lab-manager

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables

**Option A: Command Prompt (temporary)**
```cmd
set DB_HOST="your host ID"
set DB_PORT="your DB port no."
set DB_NAME="your DB name"
set DB_USER="your DB User name"
set DB_PASSWORD="your_password"
```

**Option B: PowerShell (temporary)**
```powershell
$env:DB_HOST="your host ID"
$env:DB_PORT="your DB port no."
$env:DB_NAME="your DB name"
$env:DB_USER="your DB User name"
$env:DB_PASSWORD="your_password"
```

**Option C: Create a batch script (permanent)**

Create a file named `run.bat`:
```cmd
@echo off
set DB_HOST=your host ID
set DB_PORT=your DB port no.
set DB_NAME=your DB name
set DB_USER=your DB User name
set DB_PASSWORD=your_password
python app.py
```

---

### Windows with WSL (Ubuntu)

#### Step 1: Install WSL (if not already installed)

```powershell
# Run in PowerShell as Administrator
wsl --install
# Restart your computer
```

#### Step 2: Install Python in WSL

```bash
# Update package list
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Verify installation
python3 --version
pip3 --version
```

#### Step 3: Install PostgreSQL in WSL

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Start PostgreSQL service
sudo service postgresql start

# Enable auto-start (add to ~/.bashrc)
echo "sudo service postgresql start" >> ~/.bashrc
```

#### Step 4: Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/AkashDeore15/research-lab-manager.git
cd research-lab-manager

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 5: Configure Environment Variables

```bash
# Add to ~/.bashrc for persistence
echo 'export DB_HOST=localhost' >> ~/.bashrc
echo 'export DB_PORT=5432' >> ~/.bashrc
echo 'export DB_NAME=research_lab_manager' >> ~/.bashrc
echo 'export DB_USER=postgres' >> ~/.bashrc
echo 'export DB_PASSWORD=postgres' >> ~/.bashrc

# Reload bashrc
source ~/.bashrc
```

---

### macOS

#### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Python

```bash
# Install Python
brew install python

# Verify installation
python3 --version
pip3 --version
```

#### Step 3: Install PostgreSQL

```bash
# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Verify installation
psql --version
```

#### Step 4: Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/AkashDeore15/research-lab-manager.git
cd research-lab-manager

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 5: Configure Environment Variables

```bash
# Add to ~/.zshrc (or ~/.bashrc)
echo 'export DB_HOST=localhost' >> ~/.zshrc
echo 'export DB_PORT=5432' >> ~/.zshrc
echo 'export DB_NAME=research_lab_manager' >> ~/.zshrc
echo 'export DB_USER=postgres' >> ~/.zshrc
echo 'export DB_PASSWORD=postgres' >> ~/.zshrc

# Reload
source ~/.zshrc
```

---

### Linux (Ubuntu/Debian)

#### Step 1: Install Python

```bash
# Update packages
sudo apt update
sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Verify installation
python3 --version
pip3 --version
```

#### Step 2: Install PostgreSQL

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
psql --version
```

#### Step 3: Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/AkashDeore15/research-lab-manager.git
cd research-lab-manager

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables

```bash
# Add to ~/.bashrc
cat >> ~/.bashrc << 'EOF'
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=research_lab_manager
export DB_USER=postgres
export DB_PASSWORD=postgres
EOF

# Reload
source ~/.bashrc
```

---

## 🗄 Database Setup

After installing PostgreSQL and the project dependencies, follow these steps to set up the database:

### Step 1: Create Database

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# In the PostgreSQL prompt, run:
```

```sql
-- Set password for postgres user (if not already set)
ALTER USER postgres PASSWORD 'postgres';

-- Create the database
CREATE DATABASE research_lab_manager;

-- Verify creation
\l

-- Exit
\q
```

### Step 2: Run Schema

```bash
# Navigate to project directory
cd research-lab-manager

# Run schema file
sudo -u postgres psql -d research_lab_manager -f schema.sql
```

### Step 3: Populate Sample Data

```bash
# Run populate file
sudo -u postgres psql -d research_lab_manager -f populate.sql
```

### Step 4: Verify Setup

```bash
# Check if data was loaded
sudo -u postgres psql -d research_lab_manager -c "SELECT COUNT(*) as members FROM lab_member;"
sudo -u postgres psql -d research_lab_manager -c "SELECT COUNT(*) as projects FROM project;"
```

Expected output:
```
 members 
---------
      25

 projects 
----------
       10
```

---

## ▶️ Running the Application

### Quick Start

```bash
# Activate virtual environment (if using)
source venv/bin/activate  # Linux/macOS/WSL
# or
venv\Scripts\activate     # Windows

# Run the application
python app.py             # Windows
python3 app.py            # Linux/macOS/WSL
```

### Expected Output

```
============================================================
  RESEARCH LAB MANAGER
============================================================
Initializing...

Testing database connection...
[SUCCESS] Database connection successful!

Press Enter to continue...
```

---

## 📁 Project Structure

```
research-lab-manager/
│
├── app.py              # Main application with menu-driven CLI
├── schema.sql          # Database schema (tables, triggers, views, indexes)
├── populate.sql        # Sample data for testing
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🗂 Database Schema

### Entity Tables

| Table | Description |
|-------|-------------|
| `LAB_MEMBER` | Base table for all members (MID, Name, Type, JoinDate) |
| `FACULTY` | Faculty-specific data (Department) |
| `STUDENT` | Student-specific data (SID, Level, Major) |
| `COLLABORATOR` | External collaborator data (Affiliation, Biography) |
| `PROJECT` | Research projects (Title, Dates, Status, Leader) |
| `GRANT_TABLE` | Funding grants (Source, Budget, Duration) |
| `EQUIPMENT` | Lab equipment (Name, Type, Status) |
| `PUBLICATION` | Research publications (Title, Date, Venue, DOI) |

### Relationship Tables

| Table | Description |
|-------|-------------|
| `WORKS` | Member-Project assignments (Role, Hours) |
| `FUNDS` | Grant-Project funding relationships |
| `MENTORS` | Mentorship relationships between members |
| `USES` | Equipment usage records (Purpose, Dates) |
| `PUBLISHES` | Member-Publication authorship |

### Business Rules (Enforced via Triggers)

1. ✅ Project leader must be a faculty member
2. ✅ Equipment cannot have more than 3 simultaneous users
3. ✅ A mentee can have only one active mentor
4. ✅ Students cannot mentor faculty members
5. ✅ Member type must match specialization table

---

## 📱 Application Features

### Main Menu
```
============================================================
  RESEARCH LAB MANAGER
============================================================

1. Project and Member Management
2. Equipment Usage Tracking
3. Grant and Publication Reporting
0. Exit
```

### Menu Navigation

```
MAIN MENU
├── 1. Project and Member Management
│   ├── 1-6:   Member CRUD operations
│   ├── 7-11:  Project CRUD operations
│   ├── 12:    Show members by grant
│   └── 13:    Show mentorship by project
│
├── 2. Equipment Usage Tracking
│   ├── 1-5:   Equipment CRUD operations
│   ├── 6:     Record new usage
│   ├── 7:     Update/End usage
│   └── 8:     Show current users & projects
│
└── 3. Grant and Publication Reporting
    ├── 1:     List all publications
    ├── 2:     List all grants
    ├── 3:     Most publications member
    ├── 4:     Avg publications by major
    ├── 5:     Funded projects in period
    └── 6:     Top 3 prolific by grant
```

---

## 📸 Screenshots

### Member Listing
```
--- All Lab Members ---
+-------+----------------------+-------------+-------------+-------------------------+
|   mid | name                 | type        | join_date   | details                 |
+=======+======================+=============+=============+=========================+
|     1 | Dr. Sarah Chen       | Faculty     | 2018-08-15  | Computer Science        |
|     2 | Dr. Michael Rodriguez| Faculty     | 2019-01-10  | Electrical Engineering  |
|     3 | Dr. Emily Watson     | Faculty     | 2020-03-20  | Computer Science        |
...
+-------+----------------------+-------------+-------------+-------------------------+
```

### Grant Listing
```
--- Grants ---
+-------+-------------------------------------+----------------+
|   gid | source                              | budget         |
+=======+=====================================+================+
|     1 | National Science Foundation (NSF)   | $500,000.00    |
|     2 | Department of Energy (DOE)          | $750,000.00    |
|     3 | DARPA                               | $1,200,000.00  |
+-------+-------------------------------------+----------------+
```

### Project Status
```
============================================================
  Project: Deep Learning for Medical Image Analysis
============================================================
  ID: 1
  Status: Active
  Start Date: 2023-02-01
  End Date: Ongoing
  Expected Duration: 24 months
  Leader: Dr. Sarah Chen (Computer Science)

--- Team Members ---
+------------------+----------+---------------------+-------+
| name             | type     | role                | hours |
+==================+==========+=====================+=======+
| Dr. Sarah Chen   | Faculty  | Principal Investigator | 15.0 |
| Alex Johnson     | Student  | Research Assistant  | 20.0  |
+------------------+----------+---------------------+-------+
```

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `Connection refused` | Start PostgreSQL: `sudo service postgresql start` (WSL/Linux) |
| `Database does not exist` | Create database: `CREATE DATABASE research_lab_manager;` |
| `Password authentication failed` | Check DB_PASSWORD environment variable |
| `Role does not exist` | Use correct username (usually `postgres`) |
| `Module not found` | Install dependencies: `pip install -r requirements.txt` |
| `Permission denied` | Use `sudo -u postgres` for PostgreSQL commands |

### WSL-Specific Issues

```bash
# If PostgreSQL won't start in WSL
sudo service postgresql start

# If you get "peer authentication failed"
sudo -u postgres psql
ALTER USER postgres PASSWORD 'postgres';
\q
```

### Check PostgreSQL Status

```bash
# Linux/WSL
sudo service postgresql status

# macOS
brew services list

# Windows
# Check Services app for "postgresql-x64-15"
```

### Reset Database

```bash
# Drop and recreate database
sudo -u postgres psql -c "DROP DATABASE IF EXISTS research_lab_manager;"
sudo -u postgres psql -c "CREATE DATABASE research_lab_manager;"
sudo -u postgres psql -d research_lab_manager -f schema.sql
sudo -u postgres psql -d research_lab_manager -f populate.sql
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is developed for educational purposes as part of a Data Management Systems Design course.

---

## 👤 Author

**Akash Deore**
- GitHub: [@AkashDeore15](https://github.com/AkashDeore15)

---

## 🙏 Acknowledgments

- NJIT Data Management Systems Design Course
- PostgreSQL Documentation
- Python psycopg2 Library

---

<p align="center">
  Made with ❤️ for Database Learning
</p>
