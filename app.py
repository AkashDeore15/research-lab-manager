"""
Research Lab Manager - Database Application
A comprehensive database system for managing university research laboratory operations.
"""

import psycopg2
from psycopg2 import sql, Error
from psycopg2.extras import RealDictCursor
from datetime import datetime, date
from decimal import Decimal
import os
from typing import Optional, List, Dict, Any, Tuple
from tabulate import tabulate


class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'research_lab_manager')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'postgres')


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig = None):
        self.config = config or DatabaseConfig()
        self.connection = None
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password
            )
            return self.connection
        except Error as e:
            print(f"\n[ERROR] Error connecting to database: {e}")
            raise
    
    def __enter__(self):
        self.connect()
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
            self.connection.close()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_subheader(title: str):
    print(f"\n--- {title} ---")

def print_success(message: str):
    print(f"\n[SUCCESS] {message}")

def print_error(message: str):
    print(f"\n[ERROR] {message}")

def print_warning(message: str):
    print(f"\n[WARNING] {message}")

def print_info(message: str):
    print(f"\n[INFO] {message}")

def format_value(value: Any, default: str = "N/A") -> str:
    """Format a value for display, handling None, Decimal, float, and date values."""
    if value is None:
        return default
    if isinstance(value, Decimal):
        return f"${value:,.2f}" if value >= 1000 else f"${value:.2f}"
    if isinstance(value, float):
        return f"${value:,.2f}" if value >= 1000 else f"${value:.2f}"
    if isinstance(value, date):
        return value.strftime('%Y-%m-%d')
    return str(value)


def format_currency(value: Any, default: str = "N/A") -> str:
    """Format a value as currency."""
    if value is None:
        return default
    try:
        num_val = float(value)
        return f"${num_val:,.2f}"
    except (ValueError, TypeError):
        return str(value)

def get_input(prompt: str, allow_empty: bool = False) -> str:
    while True:
        try:
            value = input(prompt).strip()
            if value or allow_empty:
                return value
            print("Input cannot be empty. Please try again.")
        except (EOFError, KeyboardInterrupt):
            return ""

def get_int_input(prompt: str, min_val: int = None, max_val: int = None, allow_empty: bool = False) -> Optional[int]:
    while True:
        try:
            value = input(prompt).strip()
            if not value and allow_empty:
                return None
            int_val = int(value)
            if min_val is not None and int_val < min_val:
                print(f"Value must be at least {min_val}.")
                continue
            if max_val is not None and int_val > max_val:
                print(f"Value must be at most {max_val}.")
                continue
            return int_val
        except ValueError:
            print("Please enter a valid integer.")
        except (EOFError, KeyboardInterrupt):
            return None

def get_float_input(prompt: str, min_val: float = None, max_val: float = None, allow_empty: bool = False) -> Optional[float]:
    while True:
        try:
            value = input(prompt).strip()
            if not value and allow_empty:
                return None
            float_val = float(value)
            if min_val is not None and float_val < min_val:
                print(f"Value must be at least {min_val}.")
                continue
            if max_val is not None and float_val > max_val:
                print(f"Value must be at most {max_val}.")
                continue
            return float_val
        except ValueError:
            print("Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            return None

def get_date_input(prompt: str, allow_empty: bool = False) -> Optional[date]:
    while True:
        try:
            value = input(prompt).strip()
            if not value and allow_empty:
                return None
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")
        except (EOFError, KeyboardInterrupt):
            return None

def get_choice(prompt: str, choices: List[str], allow_empty: bool = False) -> Optional[str]:
    choices_lower = [c.lower() for c in choices]
    while True:
        try:
            value = input(prompt).strip()
            if not value and allow_empty:
                return None
            if value.lower() in choices_lower:
                return choices[choices_lower.index(value.lower())]
            print(f"Please enter one of: {', '.join(choices)}")
        except (EOFError, KeyboardInterrupt):
            return None

def format_table(data: List[Dict], headers: List[str] = None) -> str:
    """Format data as a table, properly handling all data types."""
    if not data:
        return "No data found."
    if headers is None:
        headers = list(data[0].keys())
    rows = []
    for row in data:
        formatted_row = []
        for h in headers:
            value = row.get(h, row.get(h.lower(), ''))
            # Format based on type
            if value is None:
                formatted_row.append('N/A')
            elif isinstance(value, Decimal) or isinstance(value, float):
                # Check if this looks like a currency/budget field
                if 'budget' in h.lower() or 'cost' in h.lower() or 'price' in h.lower():
                    formatted_row.append(f"${float(value):,.2f}")
                else:
                    formatted_row.append(f"{float(value):,.2f}")
            elif isinstance(value, date):
                formatted_row.append(value.strftime('%Y-%m-%d'))
            else:
                formatted_row.append(value)
        rows.append(formatted_row)
    return tabulate(rows, headers=headers, tablefmt='grid')

def confirm_action(prompt: str = "Are you sure? (y/n): ") -> bool:
    try:
        response = input(prompt).strip().lower()
        return response in ('y', 'yes')
    except (EOFError, KeyboardInterrupt):
        return False

def pause():
    try:
        input("\nPress Enter to continue...")
    except (EOFError, KeyboardInterrupt):
        pass


class QueryExecutor:
    def __init__(self, config: DatabaseConfig = None):
        self.config = config or DatabaseConfig()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True) -> Tuple[bool, Any]:
        try:
            with DatabaseConnection(self.config) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, params)
                    if fetch:
                        results = cur.fetchall()
                        return True, [dict(row) for row in results]
                    return True, cur.rowcount
        except Error as e:
            return False, str(e)
    
    def execute_insert(self, query: str, params: tuple = None) -> Tuple[bool, Any]:
        try:
            with DatabaseConnection(self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    try:
                        result = cur.fetchone()
                        return True, result[0] if result else None
                    except:
                        return True, None
        except Error as e:
            return False, str(e)
    
    def execute_update(self, query: str, params: tuple = None) -> Tuple[bool, int]:
        try:
            with DatabaseConnection(self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    return True, cur.rowcount
        except Error as e:
            return False, str(e)


class MemberManager:
    def __init__(self, executor: QueryExecutor):
        self.executor = executor
    
    def list_all_members(self) -> None:
        query = """
            SELECT lm.MID AS mid, lm.Name AS name, lm.MType AS type,
                   lm.JoinDate AS join_date,
                   COALESCE(f.Department, s.Major, c.Affiliation) AS details
            FROM LAB_MEMBER lm
            LEFT JOIN FACULTY f ON lm.MID = f.MID
            LEFT JOIN STUDENT s ON lm.MID = s.MID
            LEFT JOIN COLLABORATOR c ON lm.MID = c.MID
            ORDER BY lm.MID
        """
        success, result = self.executor.execute_query(query)
        if success:
            print_subheader("All Lab Members")
            print(format_table(result, ['mid', 'name', 'type', 'join_date', 'details']) if result else "No members found.")
        else:
            print_error(f"Failed to retrieve members: {result}")
    
    def search_members(self) -> None:
        print_subheader("Search Members")
        print("1. Search by name\n2. Search by type\n3. Search by department/major/affiliation")
        choice = get_int_input("Enter choice (1-3): ", 1, 3)
        if choice is None:
            return
        
        if choice == 1:
            name = get_input("Enter name to search: ")
            if not name: return
            query = "SELECT lm.MID AS mid, lm.Name AS name, lm.MType AS type FROM LAB_MEMBER lm WHERE LOWER(lm.Name) LIKE LOWER(%s) ORDER BY lm.Name"
            params = (f'%{name}%',)
        elif choice == 2:
            mtype = get_choice("Enter type (Faculty/Student/Collaborator): ", ['Faculty', 'Student', 'Collaborator'])
            if not mtype: return
            query = "SELECT lm.MID AS mid, lm.Name AS name, lm.MType AS type FROM LAB_MEMBER lm WHERE lm.MType = %s ORDER BY lm.Name"
            params = (mtype,)
        else:
            search_term = get_input("Enter department/major/affiliation to search: ")
            if not search_term: return
            query = """SELECT lm.MID AS mid, lm.Name AS name, lm.MType AS type,
                       COALESCE(f.Department, s.Major, c.Affiliation) AS details
                       FROM LAB_MEMBER lm LEFT JOIN FACULTY f ON lm.MID = f.MID
                       LEFT JOIN STUDENT s ON lm.MID = s.MID LEFT JOIN COLLABORATOR c ON lm.MID = c.MID
                       WHERE LOWER(COALESCE(f.Department, s.Major, c.Affiliation, '')) LIKE LOWER(%s) ORDER BY lm.Name"""
            params = (f'%{search_term}%',)
        
        success, result = self.executor.execute_query(query, params)
        if success:
            print(format_table(result) if result else "No members found matching your search.")
        else:
            print_error(f"Search failed: {result}")
    
    def get_member_details(self, mid: int = None) -> Optional[Dict]:
        if mid is None:
            mid = get_int_input("Enter Member ID: ", min_val=1)
            if mid is None: return None
        
        query = """SELECT lm.MID AS mid, lm.Name AS name, lm.MType AS type, lm.JoinDate AS join_date,
                   f.Department AS department, s.SID AS student_id, s.Level AS level, s.Major AS major,
                   c.Affiliation AS affiliation, c.Biography AS biography
                   FROM LAB_MEMBER lm LEFT JOIN FACULTY f ON lm.MID = f.MID
                   LEFT JOIN STUDENT s ON lm.MID = s.MID LEFT JOIN COLLABORATOR c ON lm.MID = c.MID
                   WHERE lm.MID = %s"""
        success, result = self.executor.execute_query(query, (mid,))
        
        if success and result:
            m = result[0]
            print_subheader(f"Member Details - {format_value(m.get('name'))}")
            print(f"  ID: {format_value(m.get('mid'))}\n  Name: {format_value(m.get('name'))}")
            print(f"  Type: {format_value(m.get('type'))}\n  Join Date: {format_value(m.get('join_date'))}")
            
            mtype = m.get('type')
            if mtype == 'Faculty':
                print(f"  Department: {format_value(m.get('department'))}")
            elif mtype == 'Student':
                print(f"  Student ID: {format_value(m.get('student_id'))}\n  Level: {format_value(m.get('level'))}\n  Major: {format_value(m.get('major'))}")
            elif mtype == 'Collaborator':
                print(f"  Affiliation: {format_value(m.get('affiliation'))}\n  Biography: {format_value(m.get('biography'), 'Not provided')}")
            
            proj_query = "SELECT p.Title AS title, w.Role AS role, w.Hours AS hours, p.Status AS status FROM WORKS w JOIN PROJECT p ON w.PID = p.PID WHERE w.MID = %s ORDER BY p.Status, p.Title"
            success2, projects = self.executor.execute_query(proj_query, (mid,))
            if success2 and projects:
                print_subheader("Projects")
                print(format_table(projects, ['title', 'role', 'hours', 'status']))
            else:
                print_info("No projects assigned.")
            return m
        else:
            print_error(f"Member with ID {mid} not found.")
            return None
    
    def add_member(self) -> None:
        print_subheader("Add New Member")
        name = get_input("Enter name: ")
        if not name: return
        mtype = get_choice("Enter type (Faculty/Student/Collaborator): ", ['Faculty', 'Student', 'Collaborator'])
        if not mtype: return
        join_date = get_date_input("Enter join date (YYYY-MM-DD) or press Enter for today: ", allow_empty=True) or date.today()
        
        query = "INSERT INTO LAB_MEMBER (Name, MType, JoinDate) VALUES (%s, %s, %s) RETURNING MID"
        success, mid = self.executor.execute_insert(query, (name, mtype, join_date))
        if not success:
            print_error(f"Failed to add member: {mid}")
            return
        
        success2 = False
        if mtype == 'Faculty':
            dept = get_input("Enter department: ")
            if dept:
                success2, _ = self.executor.execute_update("INSERT INTO FACULTY (MID, Department) VALUES (%s, %s)", (mid, dept))
        elif mtype == 'Student':
            sid = get_input("Enter student ID: ")
            level = get_choice("Enter level (Freshman/Sophomore/Junior/Senior/Graduate): ", ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate'])
            major = get_input("Enter major: ")
            if sid and level and major:
                success2, _ = self.executor.execute_update("INSERT INTO STUDENT (MID, SID, Level, Major) VALUES (%s, %s, %s, %s)", (mid, sid, level, major))
        else:
            affil = get_input("Enter affiliation: ")
            bio = get_input("Enter biography (or press Enter to skip): ", allow_empty=True)
            if affil:
                success2, _ = self.executor.execute_update("INSERT INTO COLLABORATOR (MID, Affiliation, Biography) VALUES (%s, %s, %s)", (mid, affil, bio or None))
        
        if success2:
            print_success(f"Member '{name}' added with ID {mid}")
        else:
            print_warning("Member created but details may be incomplete.")
    
    def update_member(self) -> None:
        mid = get_int_input("Enter Member ID to update: ", min_val=1)
        if mid is None: return
        
        success, result = self.executor.execute_query("SELECT MID, Name, MType FROM LAB_MEMBER WHERE MID = %s", (mid,))
        if not success or not result:
            print_error(f"Member with ID {mid} not found.")
            return
        
        m = result[0]
        print(f"\nCurrent: {format_value(m.get('name'))} ({format_value(m.get('mtype'))})")
        print("1. Update Name\n2. Update Type-specific details")
        choice = get_int_input("Enter choice (1-2): ", 1, 2)
        if choice is None: return
        
        if choice == 1:
            new_name = get_input("Enter new name: ")
            if new_name:
                success, _ = self.executor.execute_update("UPDATE LAB_MEMBER SET Name = %s WHERE MID = %s", (new_name, mid))
                print_success("Name updated.") if success else print_error("Update failed.")
        else:
            mtype = m.get('mtype')
            if mtype == 'Faculty':
                dept = get_input("Enter new department: ")
                if dept:
                    self.executor.execute_update("UPDATE FACULTY SET Department = %s WHERE MID = %s", (dept, mid))
            elif mtype == 'Student':
                level = get_choice("Enter new level: ", ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate'])
                major = get_input("Enter new major: ")
                if level: self.executor.execute_update("UPDATE STUDENT SET Level = %s WHERE MID = %s", (level, mid))
                if major: self.executor.execute_update("UPDATE STUDENT SET Major = %s WHERE MID = %s", (major, mid))
            else:
                affil = get_input("Enter new affiliation: ")
                if affil: self.executor.execute_update("UPDATE COLLABORATOR SET Affiliation = %s WHERE MID = %s", (affil, mid))
            print_success("Details updated.")
    
    def remove_member(self) -> None:
        mid = get_int_input("Enter Member ID to remove: ", min_val=1)
        if mid is None: return
        
        success, result = self.executor.execute_query("SELECT Name, MType FROM LAB_MEMBER WHERE MID = %s", (mid,))
        if not success or not result:
            print_error(f"Member with ID {mid} not found.")
            return
        
        m = result[0]
        print(f"\nMember to remove: {format_value(m.get('name'))} ({format_value(m.get('mtype'))})")
        print_warning("This will remove all associated records.")
        
        if confirm_action():
            success, _ = self.executor.execute_update("DELETE FROM LAB_MEMBER WHERE MID = %s", (mid,))
            print_success("Member removed.") if success else print_error("Failed to remove member.")
        else:
            print_info("Operation cancelled.")


class ProjectManager:
    def __init__(self, executor: QueryExecutor):
        self.executor = executor
    
    def list_all_projects(self) -> None:
        query = """SELECT p.PID AS pid, p.Title AS title, p.Status AS status,
                   p.SDate AS start_date, p.EDate AS end_date, COALESCE(lm.Name, 'Unassigned') AS leader
                   FROM PROJECT p LEFT JOIN LAB_MEMBER lm ON p.LeaderMID = lm.MID
                   ORDER BY p.Status, p.SDate DESC"""
        success, result = self.executor.execute_query(query)
        if success:
            print_subheader("All Projects")
            print(format_table(result, ['pid', 'title', 'status', 'start_date', 'end_date', 'leader']) if result else "No projects found.")
        else:
            print_error(f"Failed to retrieve projects: {result}")
    
    def get_project_status(self) -> None:
        pid = get_int_input("Enter Project ID: ", min_val=1)
        if pid is None: return
        
        query = """SELECT p.PID AS pid, p.Title AS title, p.Status AS status, p.SDate AS start_date,
                   p.EDate AS end_date, p.EDuration AS expected_duration,
                   lm.Name AS leader_name, f.Department AS leader_dept
                   FROM PROJECT p LEFT JOIN LAB_MEMBER lm ON p.LeaderMID = lm.MID
                   LEFT JOIN FACULTY f ON p.LeaderMID = f.MID WHERE p.PID = %s"""
        success, result = self.executor.execute_query(query, (pid,))
        
        if not success or not result:
            print_error(f"Project with ID {pid} not found.")
            return
        
        p = result[0]
        print_header(f"Project: {format_value(p.get('title'))}")
        print(f"  ID: {format_value(p.get('pid'))}\n  Status: {format_value(p.get('status'))}")
        print(f"  Start Date: {format_value(p.get('start_date'))}\n  End Date: {format_value(p.get('end_date'), 'Ongoing')}")
        print(f"  Expected Duration: {format_value(p.get('expected_duration'), 'N/A')} months")
        print(f"  Leader: {format_value(p.get('leader_name'), 'Unassigned')} ({format_value(p.get('leader_dept'), 'N/A')})")
        
        team_query = "SELECT lm.Name AS name, lm.MType AS type, w.Role AS role, w.Hours AS hours FROM WORKS w JOIN LAB_MEMBER lm ON w.MID = lm.MID WHERE w.PID = %s ORDER BY w.Role"
        success2, team = self.executor.execute_query(team_query, (pid,))
        if success2 and team:
            print_subheader("Team Members")
            print(format_table(team, ['name', 'type', 'role', 'hours']))
            print(f"Total: {len(team)} members")
        else:
            print_info("No team members assigned.")
        
        fund_query = "SELECT g.Source AS source, g.Budget AS budget FROM FUNDS f JOIN GRANT_TABLE g ON f.GID = g.GID WHERE f.PID = %s"
        success3, funding = self.executor.execute_query(fund_query, (pid,))
        if success3 and funding:
            print_subheader("Funding")
            print(format_table(funding, ['source', 'budget']))
            total = sum((f.get('budget') or 0) for f in funding)
            print(f"Total: ${total:,.2f}")
        else:
            print_info("No funding sources.")
    
    def add_project(self) -> None:
        print_subheader("Add New Project")
        title = get_input("Enter title: ")
        if not title: return
        start_date = get_date_input("Enter start date (YYYY-MM-DD): ")
        if not start_date: return
        end_date = get_date_input("Enter end date (or press Enter for ongoing): ", allow_empty=True)
        duration = get_int_input("Enter expected duration (months): ", min_val=1)
        if duration is None: return
        status = get_choice("Enter status (Active/Completed/Paused): ", ['Active', 'Completed', 'Paused'])
        if not status: return
        
        faculty_query = "SELECT lm.MID AS mid, lm.Name AS name, f.Department AS dept FROM LAB_MEMBER lm JOIN FACULTY f ON lm.MID = f.MID ORDER BY lm.Name"
        success, faculty = self.executor.execute_query(faculty_query)
        if success and faculty:
            print("\nAvailable Faculty:")
            print(format_table(faculty, ['mid', 'name', 'dept']))
            leader = get_int_input("Enter Leader MID: ", min_val=1)
            if leader is None: return
        else:
            print_error("No faculty found.")
            return
        
        query = "INSERT INTO PROJECT (Title, SDate, EDate, EDuration, Status, LeaderMID) VALUES (%s, %s, %s, %s, %s, %s) RETURNING PID"
        success, pid = self.executor.execute_insert(query, (title, start_date, end_date, duration, status, leader))
        if success:
            print_success(f"Project '{title}' created with ID {pid}")
            if confirm_action("Assign team members now? (y/n): "):
                self._assign_team(pid)
        else:
            print_error(f"Failed to create project: {pid}")
    
    def _assign_team(self, pid: int) -> None:
        while True:
            mid = get_int_input("Enter Member ID (0 to finish): ", min_val=0)
            if mid is None or mid == 0: break
            role = get_input("Enter role: ")
            if not role: continue
            hours = get_float_input("Enter weekly hours: ", min_val=0, max_val=168)
            if hours is None: continue
            query = "INSERT INTO WORKS (MID, PID, Role, Hours) VALUES (%s, %s, %s, %s) ON CONFLICT (MID, PID) DO UPDATE SET Role = EXCLUDED.Role, Hours = EXCLUDED.Hours"
            success, _ = self.executor.execute_update(query, (mid, pid, role, hours))
            print_success(f"Member {mid} assigned.") if success else print_error("Assignment failed.")
    
    def update_project(self) -> None:
        pid = get_int_input("Enter Project ID: ", min_val=1)
        if pid is None: return
        
        success, result = self.executor.execute_query("SELECT Title, Status FROM PROJECT WHERE PID = %s", (pid,))
        if not success or not result:
            print_error(f"Project with ID {pid} not found.")
            return
        
        p = result[0]
        print(f"\nCurrent: {format_value(p.get('title'))} ({format_value(p.get('status'))})")
        print("1. Title\n2. Status\n3. End Date\n4. Leader\n5. Team")
        choice = get_int_input("Update (1-5): ", 1, 5)
        if choice is None: return
        
        if choice == 1:
            new_title = get_input("New title: ")
            if new_title:
                self.executor.execute_update("UPDATE PROJECT SET Title = %s WHERE PID = %s", (new_title, pid))
                print_success("Title updated.")
        elif choice == 2:
            new_status = get_choice("New status (Active/Completed/Paused): ", ['Active', 'Completed', 'Paused'])
            if new_status:
                self.executor.execute_update("UPDATE PROJECT SET Status = %s WHERE PID = %s", (new_status, pid))
                print_success("Status updated.")
        elif choice == 3:
            new_date = get_date_input("New end date (or Enter to clear): ", allow_empty=True)
            self.executor.execute_update("UPDATE PROJECT SET EDate = %s WHERE PID = %s", (new_date, pid))
            print_success("End date updated.")
        elif choice == 4:
            faculty_query = "SELECT lm.MID AS mid, lm.Name AS name FROM LAB_MEMBER lm JOIN FACULTY f ON lm.MID = f.MID ORDER BY lm.Name"
            success, faculty = self.executor.execute_query(faculty_query)
            if success and faculty:
                print(format_table(faculty, ['mid', 'name']))
                new_leader = get_int_input("New Leader MID: ", min_val=1)
                if new_leader:
                    self.executor.execute_update("UPDATE PROJECT SET LeaderMID = %s WHERE PID = %s", (new_leader, pid))
                    print_success("Leader updated.")
        else:
            self._assign_team(pid)
    
    def remove_project(self) -> None:
        pid = get_int_input("Enter Project ID: ", min_val=1)
        if pid is None: return
        
        success, result = self.executor.execute_query("SELECT Title FROM PROJECT WHERE PID = %s", (pid,))
        if not success or not result:
            print_error(f"Project with ID {pid} not found.")
            return
        
        print(f"\nProject: {format_value(result[0].get('title'))}")
        print_warning("This will remove all work assignments and funding.")
        
        if confirm_action():
            success, _ = self.executor.execute_update("DELETE FROM PROJECT WHERE PID = %s", (pid,))
            print_success("Project removed.") if success else print_error("Failed.")
        else:
            print_info("Cancelled.")
    
    def show_members_by_grant(self) -> None:
        grants_query = "SELECT GID AS gid, Source AS source, Budget AS budget FROM GRANT_TABLE ORDER BY GID"
        success, grants = self.executor.execute_query(grants_query)
        if success and grants:
            print_subheader("Grants")
            print(format_table(grants, ['gid', 'source', 'budget']))
        else:
            print_info("No grants found.")
            return
        
        gid = get_int_input("Enter Grant ID: ", min_val=1)
        if gid is None: return
        
        query = """SELECT DISTINCT lm.MID AS mid, lm.Name AS name, lm.MType AS type, p.Title AS project, w.Role AS role
                   FROM GRANT_TABLE g JOIN FUNDS f ON g.GID = f.GID JOIN PROJECT p ON f.PID = p.PID
                   JOIN WORKS w ON p.PID = w.PID JOIN LAB_MEMBER lm ON w.MID = lm.MID
                   WHERE g.GID = %s ORDER BY p.Title, lm.Name"""
        success, result = self.executor.execute_query(query, (gid,))
        if success and result:
            print_subheader(f"Members for Grant {gid}")
            print(format_table(result, ['mid', 'name', 'type', 'project', 'role']))
        else:
            print_info("No members found.")
    
    def show_mentorship_by_project(self) -> None:
        proj_query = "SELECT PID AS pid, Title AS title FROM PROJECT ORDER BY PID"
        success, projects = self.executor.execute_query(proj_query)
        if success and projects:
            print_subheader("Projects")
            print(format_table(projects, ['pid', 'title']))
        else:
            print_info("No projects found.")
            return
        
        pid = get_int_input("Enter Project ID: ", min_val=1)
        if pid is None: return
        
        query = """SELECT mentor.Name AS mentor, mentor.MType AS mentor_type, mentee.Name AS mentee, mentee.MType AS mentee_type,
                   m.StartDate AS start_date, m.EndDate AS end_date
                   FROM MENTORS m JOIN LAB_MEMBER mentor ON m.MentorMID = mentor.MID
                   JOIN LAB_MEMBER mentee ON m.MenteeMID = mentee.MID
                   WHERE m.MentorMID IN (SELECT MID FROM WORKS WHERE PID = %s)
                   AND m.MenteeMID IN (SELECT MID FROM WORKS WHERE PID = %s) ORDER BY mentor.Name"""
        success, result = self.executor.execute_query(query, (pid, pid))
        if success and result:
            print_subheader(f"Mentorship in Project {pid}")
            print(format_table(result, ['mentor', 'mentor_type', 'mentee', 'mentee_type', 'start_date', 'end_date']))
        else:
            print_info("No mentorship relations found.")


class EquipmentManager:
    def __init__(self, executor: QueryExecutor):
        self.executor = executor
    
    def list_all_equipment(self) -> None:
        query = """SELECT e.EID AS eid, e.EName AS name, e.EType AS type, e.PDate AS purchase_date, e.Status AS status,
                   COUNT(CASE WHEN u.EDate IS NULL OR u.EDate >= CURRENT_DATE THEN 1 END) AS current_users
                   FROM EQUIPMENT e LEFT JOIN USES u ON e.EID = u.EID
                   GROUP BY e.EID, e.EName, e.EType, e.PDate, e.Status ORDER BY e.EID"""
        success, result = self.executor.execute_query(query)
        if success:
            print_subheader("All Equipment")
            print(format_table(result, ['eid', 'name', 'type', 'purchase_date', 'status', 'current_users']) if result else "No equipment found.")
        else:
            print_error(f"Failed: {result}")
    
    def get_equipment_status(self) -> None:
        eid = get_int_input("Enter Equipment ID: ", min_val=1)
        if eid is None: return
        
        query = "SELECT EID AS eid, EName AS name, EType AS type, PDate AS purchase_date, Status AS status FROM EQUIPMENT WHERE EID = %s"
        success, result = self.executor.execute_query(query, (eid,))
        if not success or not result:
            print_error(f"Equipment with ID {eid} not found.")
            return
        
        e = result[0]
        print_header(f"Equipment: {format_value(e.get('name'))}")
        print(f"  ID: {format_value(e.get('eid'))}\n  Type: {format_value(e.get('type'))}")
        print(f"  Purchase Date: {format_value(e.get('purchase_date'))}\n  Status: {format_value(e.get('status'))}")
        
        users_query = """SELECT lm.Name AS name, lm.MType AS type, u.SDate AS start_date, u.Purpose AS purpose
                        FROM USES u JOIN LAB_MEMBER lm ON u.MID = lm.MID
                        WHERE u.EID = %s AND (u.EDate IS NULL OR u.EDate >= CURRENT_DATE) ORDER BY u.SDate"""
        success2, users = self.executor.execute_query(users_query, (eid,))
        if success2 and users:
            print_subheader("Current Users")
            print(format_table(users, ['name', 'type', 'start_date', 'purpose']))
            print(f"Count: {len(users)}/3")
        else:
            print_info("No current users.")
    
    def show_current_users_and_projects(self) -> None:
        eid = get_int_input("Enter Equipment ID: ", min_val=1)
        if eid is None: return
        
        query = """SELECT lm.MID AS mid, lm.Name AS name, lm.MType AS type, u.Purpose AS purpose,
                   STRING_AGG(DISTINCT p.Title, ', ') AS projects
                   FROM USES u JOIN LAB_MEMBER lm ON u.MID = lm.MID
                   LEFT JOIN WORKS w ON lm.MID = w.MID LEFT JOIN PROJECT p ON w.PID = p.PID AND p.Status = 'Active'
                   WHERE u.EID = %s AND (u.EDate IS NULL OR u.EDate >= CURRENT_DATE)
                   GROUP BY lm.MID, lm.Name, lm.MType, u.Purpose ORDER BY lm.Name"""
        success, result = self.executor.execute_query(query, (eid,))
        if success and result:
            print_subheader(f"Users of Equipment {eid} and Projects")
            print(format_table(result, ['mid', 'name', 'type', 'purpose', 'projects']))
        else:
            print_info("No current users.")
    
    def add_equipment(self) -> None:
        print_subheader("Add Equipment")
        name = get_input("Enter name: ")
        if not name: return
        etype = get_input("Enter type: ")
        if not etype: return
        pdate = get_date_input("Enter purchase date (YYYY-MM-DD): ")
        if not pdate: return
        status = get_choice("Enter status (Available/In Use/Retired): ", ['Available', 'In Use', 'Retired'])
        if not status: return
        
        query = "INSERT INTO EQUIPMENT (EName, EType, PDate, Status) VALUES (%s, %s, %s, %s) RETURNING EID"
        success, eid = self.executor.execute_insert(query, (name, etype, pdate, status))
        print_success(f"Equipment '{name}' added with ID {eid}") if success else print_error(f"Failed: {eid}")
    
    def update_equipment(self) -> None:
        eid = get_int_input("Enter Equipment ID: ", min_val=1)
        if eid is None: return
        
        success, result = self.executor.execute_query("SELECT EName AS name, Status AS status FROM EQUIPMENT WHERE EID = %s", (eid,))
        if not success or not result:
            print_error(f"Equipment with ID {eid} not found.")
            return
        
        e = result[0]
        print(f"\nCurrent: {format_value(e.get('name'))} ({format_value(e.get('status'))})")
        print("1. Name\n2. Type\n3. Status")
        choice = get_int_input("Update (1-3): ", 1, 3)
        if choice is None: return
        
        if choice == 1:
            new_name = get_input("New name: ")
            if new_name:
                self.executor.execute_update("UPDATE EQUIPMENT SET EName = %s WHERE EID = %s", (new_name, eid))
                print_success("Updated.")
        elif choice == 2:
            new_type = get_input("New type: ")
            if new_type:
                self.executor.execute_update("UPDATE EQUIPMENT SET EType = %s WHERE EID = %s", (new_type, eid))
                print_success("Updated.")
        else:
            new_status = get_choice("New status (Available/In Use/Retired): ", ['Available', 'In Use', 'Retired'])
            if new_status:
                self.executor.execute_update("UPDATE EQUIPMENT SET Status = %s WHERE EID = %s", (new_status, eid))
                print_success("Updated.")
    
    def remove_equipment(self) -> None:
        eid = get_int_input("Enter Equipment ID: ", min_val=1)
        if eid is None: return
        
        success, result = self.executor.execute_query("SELECT EName AS name FROM EQUIPMENT WHERE EID = %s", (eid,))
        if not success or not result:
            print_error(f"Equipment with ID {eid} not found.")
            return
        
        print(f"\nEquipment: {format_value(result[0].get('name'))}")
        print_warning("This will remove all usage records.")
        
        if confirm_action():
            success, _ = self.executor.execute_update("DELETE FROM EQUIPMENT WHERE EID = %s", (eid,))
            print_success("Removed.") if success else print_error("Failed.")
        else:
            print_info("Cancelled.")
    
    def add_usage(self) -> None:
        print_subheader("Record Usage")
        equip_query = "SELECT EID AS eid, EName AS name, Status AS status FROM EQUIPMENT WHERE Status != 'Retired' ORDER BY EID"
        success, equipment = self.executor.execute_query(equip_query)
        if success and equipment:
            print(format_table(equipment, ['eid', 'name', 'status']))
        
        eid = get_int_input("Equipment ID: ", min_val=1)
        if eid is None: return
        mid = get_int_input("Member ID: ", min_val=1)
        if mid is None: return
        sdate = get_date_input("Start date (or Enter for today): ", allow_empty=True) or date.today()
        edate = get_date_input("End date (or Enter for ongoing): ", allow_empty=True)
        purpose = get_input("Purpose: ")
        if not purpose: return
        
        query = "INSERT INTO USES (MID, EID, SDate, EDate, Purpose) VALUES (%s, %s, %s, %s, %s)"
        success, _ = self.executor.execute_update(query, (mid, eid, sdate, edate, purpose))
        print_success("Usage recorded.") if success else print_error("Failed.")
    
    def update_usage(self) -> None:
        print_subheader("Update Usage")
        eid = get_int_input("Equipment ID: ", min_val=1)
        if eid is None: return
        
        usage_query = """SELECT u.MID AS mid, lm.Name AS name, u.SDate AS start_date, u.Purpose AS purpose
                        FROM USES u JOIN LAB_MEMBER lm ON u.MID = lm.MID
                        WHERE u.EID = %s AND (u.EDate IS NULL OR u.EDate >= CURRENT_DATE) ORDER BY u.SDate"""
        success, usage = self.executor.execute_query(usage_query, (eid,))
        if not success or not usage:
            print_info("No active usage found.")
            return
        
        print(format_table(usage, ['mid', 'name', 'start_date', 'purpose']))
        mid = get_int_input("Member ID: ", min_val=1)
        if mid is None: return
        sdate = get_date_input("Start Date of record: ")
        if sdate is None: return
        
        print("1. End usage\n2. Update purpose")
        choice = get_int_input("Choice (1-2): ", 1, 2)
        if choice == 1:
            edate = get_date_input("End date: ")
            if edate:
                self.executor.execute_update("UPDATE USES SET EDate = %s WHERE MID = %s AND EID = %s AND SDate = %s", (edate, mid, eid, sdate))
                print_success("Updated.")
        elif choice == 2:
            purpose = get_input("New purpose: ")
            if purpose:
                self.executor.execute_update("UPDATE USES SET Purpose = %s WHERE MID = %s AND EID = %s AND SDate = %s", (purpose, mid, eid, sdate))
                print_success("Updated.")


class ReportManager:
    def __init__(self, executor: QueryExecutor):
        self.executor = executor
    
    def member_with_most_publications(self) -> None:
        query = """WITH pub_counts AS (
                    SELECT lm.MID AS mid, lm.Name AS name, lm.MType AS type, COUNT(p.PubID) AS pub_count
                    FROM LAB_MEMBER lm LEFT JOIN PUBLISHES p ON lm.MID = p.MID
                    GROUP BY lm.MID, lm.Name, lm.MType)
                   SELECT * FROM pub_counts WHERE pub_count = (SELECT MAX(pub_count) FROM pub_counts) ORDER BY name"""
        success, result = self.executor.execute_query(query)
        if success and result:
            print_subheader("Member(s) with Most Publications")
            print(format_table(result, ['mid', 'name', 'type', 'pub_count']))
        else:
            print_info("No publication data found.")
    
    def avg_publications_by_major(self) -> None:
        query = """SELECT s.Major AS major, COUNT(DISTINCT s.MID) AS students, COUNT(p.PubID) AS total_pubs,
                   ROUND(COUNT(p.PubID)::DECIMAL / NULLIF(COUNT(DISTINCT s.MID), 0), 2) AS avg_pubs
                   FROM STUDENT s LEFT JOIN PUBLISHES p ON s.MID = p.MID
                   GROUP BY s.Major ORDER BY avg_pubs DESC"""
        success, result = self.executor.execute_query(query)
        if success and result:
            print_subheader("Average Publications by Major")
            print(format_table(result, ['major', 'students', 'total_pubs', 'avg_pubs']))
        else:
            print_info("No student data found.")
    
    def funded_active_projects_in_period(self) -> None:
        print_subheader("Funded Active Projects in Period")
        start = get_date_input("Period start (YYYY-MM-DD): ")
        if start is None: return
        end = get_date_input("Period end (YYYY-MM-DD): ")
        if end is None: return
        
        query = """SELECT COUNT(DISTINCT p.PID) AS count FROM PROJECT p JOIN FUNDS f ON p.PID = f.PID
                   WHERE p.SDate <= %s AND (p.EDate IS NULL OR p.EDate >= %s)"""
        success, result = self.executor.execute_query(query, (end, start))
        if success and result:
            count = result[0].get('count', 0) or 0
            print(f"\nFunded projects active during {start} to {end}: {count}")
            
            if count > 0 and confirm_action("Show details? (y/n): "):
                detail_query = """SELECT DISTINCT p.PID AS pid, p.Title AS title, p.Status AS status,
                                 p.SDate AS start_date, p.EDate AS end_date, STRING_AGG(DISTINCT g.Source, ', ') AS grants
                                 FROM PROJECT p JOIN FUNDS f ON p.PID = f.PID JOIN GRANT_TABLE g ON f.GID = g.GID
                                 WHERE p.SDate <= %s AND (p.EDate IS NULL OR p.EDate >= %s)
                                 GROUP BY p.PID, p.Title, p.Status, p.SDate, p.EDate ORDER BY p.Title"""
                success2, details = self.executor.execute_query(detail_query, (end, start))
                if success2 and details:
                    print(format_table(details, ['pid', 'title', 'status', 'start_date', 'end_date', 'grants']))
    
    def prolific_members_by_grant(self) -> None:
        grants_query = "SELECT GID AS gid, Source AS source, Budget AS budget FROM GRANT_TABLE ORDER BY GID"
        success, grants = self.executor.execute_query(grants_query)
        if success and grants:
            print_subheader("Grants")
            print(format_table(grants, ['gid', 'source', 'budget']))
        else:
            print_info("No grants found.")
            return
        
        gid = get_int_input("Enter Grant ID: ", min_val=1)
        if gid is None: return
        
        query = """SELECT lm.MID AS mid, lm.Name AS name, lm.MType AS type, COUNT(DISTINCT pub.PubID) AS pub_count
                   FROM GRANT_TABLE g JOIN FUNDS f ON g.GID = f.GID JOIN PROJECT p ON f.PID = p.PID
                   JOIN WORKS w ON p.PID = w.PID JOIN LAB_MEMBER lm ON w.MID = lm.MID
                   LEFT JOIN PUBLISHES pub ON lm.MID = pub.MID
                   WHERE g.GID = %s GROUP BY lm.MID, lm.Name, lm.MType ORDER BY pub_count DESC LIMIT 3"""
        success, result = self.executor.execute_query(query, (gid,))
        if success and result:
            print_subheader(f"Top 3 Prolific Members for Grant {gid}")
            print(format_table(result, ['mid', 'name', 'type', 'pub_count']))
        else:
            print_info("No members found.")
    
    def list_all_publications(self) -> None:
        query = """SELECT pub.PubID AS pubid, pub.Title AS title, pub.PubDate AS date, pub.Venue AS venue,
                   COALESCE(STRING_AGG(lm.Name, ', ' ORDER BY lm.Name), 'No authors') AS authors
                   FROM PUBLICATION pub LEFT JOIN PUBLISHES p ON pub.PubID = p.PubID
                   LEFT JOIN LAB_MEMBER lm ON p.MID = lm.MID
                   GROUP BY pub.PubID, pub.Title, pub.PubDate, pub.Venue ORDER BY pub.PubDate DESC"""
        success, result = self.executor.execute_query(query)
        if success:
            print_subheader("All Publications")
            print(format_table(result, ['pubid', 'title', 'date', 'venue', 'authors']) if result else "No publications found.")
        else:
            print_error(f"Failed: {result}")
    
    def list_all_grants(self) -> None:
        query = """SELECT g.GID AS gid, g.Source AS source, g.Budget AS budget, g.StartDate AS start_date,
                   g.Duration AS duration, COALESCE(STRING_AGG(p.Title, ', '), 'None') AS projects
                   FROM GRANT_TABLE g LEFT JOIN FUNDS f ON g.GID = f.GID LEFT JOIN PROJECT p ON f.PID = p.PID
                   GROUP BY g.GID, g.Source, g.Budget, g.StartDate, g.Duration ORDER BY g.StartDate DESC"""
        success, result = self.executor.execute_query(query)
        if success:
            print_subheader("All Grants")
            print(format_table(result, ['gid', 'source', 'budget', 'start_date', 'duration', 'projects']) if result else "No grants found.")
        else:
            print_error(f"Failed: {result}")


class ResearchLabManager:
    def __init__(self):
        self.config = DatabaseConfig()
        self.executor = QueryExecutor(self.config)
        self.member_mgr = MemberManager(self.executor)
        self.project_mgr = ProjectManager(self.executor)
        self.equipment_mgr = EquipmentManager(self.executor)
        self.report_mgr = ReportManager(self.executor)
    
    def test_connection(self) -> bool:
        try:
            with DatabaseConnection(self.config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    return True
        except Exception as e:
            print_error(f"Database connection failed: {e}")
            return False
    
    def main_menu(self) -> None:
        while True:
            print_header("RESEARCH LAB MANAGER")
            print("\n1. Project and Member Management\n2. Equipment Usage Tracking\n3. Grant and Publication Reporting\n0. Exit")
            choice = get_int_input("\nChoice: ", 0, 3)
            if choice is None or choice == 0:
                print("\nGoodbye!")
                break
            elif choice == 1: self.project_member_menu()
            elif choice == 2: self.equipment_menu()
            elif choice == 3: self.report_menu()
    
    def project_member_menu(self) -> None:
        while True:
            print_header("PROJECT AND MEMBER MANAGEMENT")
            print("\n--- Members ---")
            print("1.  List all members\n2.  Search members\n3.  View member details")
            print("4.  Add member\n5.  Update member\n6.  Remove member")
            print("\n--- Projects ---")
            print("7.  List all projects\n8.  View project status\n9.  Add project")
            print("10. Update project\n11. Remove project")
            print("\n--- Special Queries ---")
            print("12. Show members by grant\n13. Show mentorship by project")
            print("\n0.  Back")
            
            choice = get_int_input("\nChoice: ", 0, 13)
            if choice is None or choice == 0: break
            
            actions = {
                1: self.member_mgr.list_all_members, 2: self.member_mgr.search_members,
                3: self.member_mgr.get_member_details, 4: self.member_mgr.add_member,
                5: self.member_mgr.update_member, 6: self.member_mgr.remove_member,
                7: self.project_mgr.list_all_projects, 8: self.project_mgr.get_project_status,
                9: self.project_mgr.add_project, 10: self.project_mgr.update_project,
                11: self.project_mgr.remove_project, 12: self.project_mgr.show_members_by_grant,
                13: self.project_mgr.show_mentorship_by_project
            }
            if choice in actions: actions[choice]()
            pause()
    
    def equipment_menu(self) -> None:
        while True:
            print_header("EQUIPMENT USAGE TRACKING")
            print("\n--- Equipment ---")
            print("1. List all equipment\n2. View equipment status\n3. Add equipment")
            print("4. Update equipment\n5. Remove equipment")
            print("\n--- Usage ---")
            print("6. Record usage\n7. Update/End usage\n8. Show users and projects")
            print("\n0. Back")
            
            choice = get_int_input("\nChoice: ", 0, 8)
            if choice is None or choice == 0: break
            
            actions = {
                1: self.equipment_mgr.list_all_equipment, 2: self.equipment_mgr.get_equipment_status,
                3: self.equipment_mgr.add_equipment, 4: self.equipment_mgr.update_equipment,
                5: self.equipment_mgr.remove_equipment, 6: self.equipment_mgr.add_usage,
                7: self.equipment_mgr.update_usage, 8: self.equipment_mgr.show_current_users_and_projects
            }
            if choice in actions: actions[choice]()
            pause()
    
    def report_menu(self) -> None:
        while True:
            print_header("GRANT AND PUBLICATION REPORTING")
            print("\n--- View Data ---")
            print("1. List all publications\n2. List all grants")
            print("\n--- Reports ---")
            print("3. Member(s) with most publications\n4. Avg publications by major")
            print("5. Funded projects in period\n6. Top 3 prolific by grant")
            print("\n0. Back")
            
            choice = get_int_input("\nChoice: ", 0, 6)
            if choice is None or choice == 0: break
            
            actions = {
                1: self.report_mgr.list_all_publications, 2: self.report_mgr.list_all_grants,
                3: self.report_mgr.member_with_most_publications, 4: self.report_mgr.avg_publications_by_major,
                5: self.report_mgr.funded_active_projects_in_period, 6: self.report_mgr.prolific_members_by_grant
            }
            if choice in actions: actions[choice]()
            pause()


def main():
    print_header("RESEARCH LAB MANAGER")
    print("Initializing...")
    
    app = ResearchLabManager()
    
    print("\nTesting database connection...")
    if not app.test_connection():
        print(f"\nCheck configuration:")
        print(f"  Host: {app.config.host}\n  Port: {app.config.port}")
        print(f"  Database: {app.config.database}\n  User: {app.config.user}")
        print("\nSet environment variables: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
        return
    
    print_success("Database connection successful!")
    pause()
    app.main_menu()


if __name__ == "__main__":
    main()