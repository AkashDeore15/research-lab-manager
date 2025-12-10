-- ============================================
-- RESEARCH LAB MANAGER DATABASE SCHEMA
-- PostgreSQL Implementation
-- ============================================

-- Drop existing tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS PUBLISHES CASCADE;
DROP TABLE IF EXISTS PUBLICATION CASCADE;
DROP TABLE IF EXISTS USES CASCADE;
DROP TABLE IF EXISTS EQUIPMENT CASCADE;
DROP TABLE IF EXISTS MENTORS CASCADE;
DROP TABLE IF EXISTS WORKS CASCADE;
DROP TABLE IF EXISTS FUNDS CASCADE;
DROP TABLE IF EXISTS PROJECT CASCADE;
DROP TABLE IF EXISTS GRANT_TABLE CASCADE;
DROP TABLE IF EXISTS FACULTY CASCADE;
DROP TABLE IF EXISTS STUDENT CASCADE;
DROP TABLE IF EXISTS COLLABORATOR CASCADE;
DROP TABLE IF EXISTS LAB_MEMBER CASCADE;

-- Drop existing types if they exist
DROP TYPE IF EXISTS member_type CASCADE;
DROP TYPE IF EXISTS project_status CASCADE;
DROP TYPE IF EXISTS equipment_status CASCADE;
DROP TYPE IF EXISTS academic_level CASCADE;

-- ============================================
-- CUSTOM TYPES (ENUMS)
-- ============================================

CREATE TYPE member_type AS ENUM ('Faculty', 'Student', 'Collaborator');
CREATE TYPE project_status AS ENUM ('Active', 'Completed', 'Paused');
CREATE TYPE equipment_status AS ENUM ('Available', 'In Use', 'Retired');
CREATE TYPE academic_level AS ENUM ('Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate');

-- ============================================
-- MAIN TABLES
-- ============================================

-- LAB_MEMBER: Base table for all lab members
CREATE TABLE LAB_MEMBER (
    MID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    MType member_type NOT NULL,
    JoinDate DATE NOT NULL DEFAULT CURRENT_DATE
);

-- FACULTY: Specialization of LAB_MEMBER
CREATE TABLE FACULTY (
    MID INTEGER PRIMARY KEY REFERENCES LAB_MEMBER(MID) ON DELETE CASCADE,
    Department VARCHAR(100) NOT NULL
);

-- STUDENT: Specialization of LAB_MEMBER
CREATE TABLE STUDENT (
    MID INTEGER PRIMARY KEY REFERENCES LAB_MEMBER(MID) ON DELETE CASCADE,
    SID VARCHAR(20) UNIQUE NOT NULL,
    Level academic_level NOT NULL,
    Major VARCHAR(100) NOT NULL
);

-- COLLABORATOR: Specialization of LAB_MEMBER
CREATE TABLE COLLABORATOR (
    MID INTEGER PRIMARY KEY REFERENCES LAB_MEMBER(MID) ON DELETE CASCADE,
    Affiliation VARCHAR(200) NOT NULL,
    Biography TEXT
);

-- GRANT_TABLE: Funding sources (named GRANT_TABLE because GRANT is a reserved word)
CREATE TABLE GRANT_TABLE (
    GID SERIAL PRIMARY KEY,
    Source VARCHAR(200) NOT NULL,
    Budget DECIMAL(15, 2) NOT NULL CHECK (Budget >= 0),
    StartDate DATE NOT NULL,
    Duration INTEGER NOT NULL CHECK (Duration > 0) -- Duration in months
);

-- PROJECT: Research projects
CREATE TABLE PROJECT (
    PID SERIAL PRIMARY KEY,
    Title VARCHAR(200) NOT NULL,
    SDate DATE NOT NULL,
    EDate DATE,
    EDuration INTEGER CHECK (EDuration > 0), -- Expected duration in months
    Status project_status NOT NULL DEFAULT 'Active',
    LeaderMID INTEGER REFERENCES LAB_MEMBER(MID) ON DELETE SET NULL,
    CONSTRAINT valid_dates CHECK (EDate IS NULL OR EDate >= SDate)
);

-- FUNDS: Relationship between GRANT and PROJECT
CREATE TABLE FUNDS (
    GID INTEGER REFERENCES GRANT_TABLE(GID) ON DELETE CASCADE,
    PID INTEGER REFERENCES PROJECT(PID) ON DELETE CASCADE,
    PRIMARY KEY (GID, PID)
);

-- WORKS: Relationship between LAB_MEMBER and PROJECT
CREATE TABLE WORKS (
    MID INTEGER REFERENCES LAB_MEMBER(MID) ON DELETE CASCADE,
    PID INTEGER REFERENCES PROJECT(PID) ON DELETE CASCADE,
    Role VARCHAR(100) NOT NULL,
    Hours DECIMAL(4, 1) NOT NULL CHECK (Hours >= 0 AND Hours <= 168), -- Weekly hours
    PRIMARY KEY (MID, PID)
);

-- MENTORS: Mentorship relationships between lab members
CREATE TABLE MENTORS (
    MentorMID INTEGER REFERENCES LAB_MEMBER(MID) ON DELETE CASCADE,
    MenteeMID INTEGER REFERENCES LAB_MEMBER(MID) ON DELETE CASCADE,
    StartDate DATE NOT NULL DEFAULT CURRENT_DATE,
    EndDate DATE,
    PRIMARY KEY (MentorMID, MenteeMID),
    CONSTRAINT no_self_mentorship CHECK (MentorMID != MenteeMID),
    CONSTRAINT valid_mentorship_dates CHECK (EndDate IS NULL OR EndDate >= StartDate)
);

-- EQUIPMENT: Lab equipment
CREATE TABLE EQUIPMENT (
    EID SERIAL PRIMARY KEY,
    EName VARCHAR(100) NOT NULL,
    EType VARCHAR(100) NOT NULL,
    PDate DATE NOT NULL, -- Purchase date
    Status equipment_status NOT NULL DEFAULT 'Available'
);

-- USES: Relationship between LAB_MEMBER and EQUIPMENT
CREATE TABLE USES (
    MID INTEGER REFERENCES LAB_MEMBER(MID) ON DELETE CASCADE,
    EID INTEGER REFERENCES EQUIPMENT(EID) ON DELETE CASCADE,
    SDate DATE NOT NULL DEFAULT CURRENT_DATE,
    EDate DATE,
    Purpose TEXT,
    PRIMARY KEY (MID, EID, SDate),
    CONSTRAINT valid_usage_dates CHECK (EDate IS NULL OR EDate >= SDate)
);

-- PUBLICATION: Research publications
CREATE TABLE PUBLICATION (
    PubID SERIAL PRIMARY KEY,
    Title VARCHAR(300) NOT NULL,
    PubDate DATE NOT NULL,
    Venue VARCHAR(200) NOT NULL,
    DOI VARCHAR(100) UNIQUE
);

-- PUBLISHES: Relationship between LAB_MEMBER and PUBLICATION
CREATE TABLE PUBLISHES (
    MID INTEGER REFERENCES LAB_MEMBER(MID) ON DELETE CASCADE,
    PubID INTEGER REFERENCES PUBLICATION(PubID) ON DELETE CASCADE,
    PRIMARY KEY (MID, PubID)
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX idx_lab_member_type ON LAB_MEMBER(MType);
CREATE INDEX idx_project_status ON PROJECT(Status);
CREATE INDEX idx_project_dates ON PROJECT(SDate, EDate);
CREATE INDEX idx_equipment_status ON EQUIPMENT(Status);
CREATE INDEX idx_publication_date ON PUBLICATION(PubDate);
CREATE INDEX idx_works_pid ON WORKS(PID);
CREATE INDEX idx_works_mid ON WORKS(MID);
CREATE INDEX idx_funds_gid ON FUNDS(GID);
CREATE INDEX idx_uses_eid ON USES(EID);

-- ============================================
-- TRIGGER FUNCTIONS AND TRIGGERS
-- ============================================

-- 1. Ensure project leader is a faculty member
CREATE OR REPLACE FUNCTION check_project_leader()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.LeaderMID IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM FACULTY WHERE MID = NEW.LeaderMID) THEN
            RAISE EXCEPTION 'Project leader must be a faculty member (MID: %)', NEW.LeaderMID;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_project_leader
BEFORE INSERT OR UPDATE ON PROJECT
FOR EACH ROW EXECUTE FUNCTION check_project_leader();

-- 2. Ensure equipment is not used by more than 3 members simultaneously
CREATE OR REPLACE FUNCTION check_equipment_usage_limit()
RETURNS TRIGGER AS $$
DECLARE
    current_users INTEGER;
BEGIN
    SELECT COUNT(*) INTO current_users
    FROM USES
    WHERE EID = NEW.EID
      AND (EDate IS NULL OR EDate >= CURRENT_DATE)
      AND SDate <= CURRENT_DATE
      AND NOT (MID = NEW.MID AND SDate = NEW.SDate); -- Exclude the current record if updating
    
    IF current_users >= 3 THEN
        RAISE EXCEPTION 'Equipment (EID: %) is already being used by 3 members simultaneously', NEW.EID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_equipment_usage_limit
BEFORE INSERT OR UPDATE ON USES
FOR EACH ROW EXECUTE FUNCTION check_equipment_usage_limit();

-- 3. Ensure a mentee has only one active mentor
CREATE OR REPLACE FUNCTION check_single_mentor()
RETURNS TRIGGER AS $$
DECLARE
    existing_mentors INTEGER;
BEGIN
    SELECT COUNT(*) INTO existing_mentors
    FROM MENTORS
    WHERE MenteeMID = NEW.MenteeMID
      AND (EndDate IS NULL OR EndDate >= CURRENT_DATE)
      AND MentorMID != NEW.MentorMID;
    
    IF existing_mentors > 0 THEN
        RAISE EXCEPTION 'Mentee (MID: %) already has an active mentor', NEW.MenteeMID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_single_mentor
BEFORE INSERT OR UPDATE ON MENTORS
FOR EACH ROW EXECUTE FUNCTION check_single_mentor();

-- 4. Ensure students cannot mentor faculty members
CREATE OR REPLACE FUNCTION check_valid_mentorship()
RETURNS TRIGGER AS $$
DECLARE
    mentor_is_student BOOLEAN;
    mentee_is_faculty BOOLEAN;
BEGIN
    SELECT EXISTS(SELECT 1 FROM STUDENT WHERE MID = NEW.MentorMID) INTO mentor_is_student;
    SELECT EXISTS(SELECT 1 FROM FACULTY WHERE MID = NEW.MenteeMID) INTO mentee_is_faculty;
    
    IF mentor_is_student AND mentee_is_faculty THEN
        RAISE EXCEPTION 'Students cannot mentor faculty members';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_valid_mentorship
BEFORE INSERT OR UPDATE ON MENTORS
FOR EACH ROW EXECUTE FUNCTION check_valid_mentorship();

-- 5. Ensure member type consistency with specialization tables
CREATE OR REPLACE FUNCTION check_member_type_on_faculty()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM LAB_MEMBER WHERE MID = NEW.MID AND MType = 'Faculty') THEN
        RAISE EXCEPTION 'Member (MID: %) is not registered as Faculty in LAB_MEMBER', NEW.MID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_faculty_type
BEFORE INSERT ON FACULTY
FOR EACH ROW EXECUTE FUNCTION check_member_type_on_faculty();

CREATE OR REPLACE FUNCTION check_member_type_on_student()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM LAB_MEMBER WHERE MID = NEW.MID AND MType = 'Student') THEN
        RAISE EXCEPTION 'Member (MID: %) is not registered as Student in LAB_MEMBER', NEW.MID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_student_type
BEFORE INSERT ON STUDENT
FOR EACH ROW EXECUTE FUNCTION check_member_type_on_student();

CREATE OR REPLACE FUNCTION check_member_type_on_collaborator()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM LAB_MEMBER WHERE MID = NEW.MID AND MType = 'Collaborator') THEN
        RAISE EXCEPTION 'Member (MID: %) is not registered as Collaborator in LAB_MEMBER', NEW.MID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_collaborator_type
BEFORE INSERT ON COLLABORATOR
FOR EACH ROW EXECUTE FUNCTION check_member_type_on_collaborator();

-- 6. Update equipment status when usage changes
CREATE OR REPLACE FUNCTION update_equipment_status()
RETURNS TRIGGER AS $$
DECLARE
    active_users INTEGER;
BEGIN
    -- For INSERT or UPDATE, check the equipment being used
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        SELECT COUNT(*) INTO active_users
        FROM USES
        WHERE EID = NEW.EID
          AND (EDate IS NULL OR EDate >= CURRENT_DATE)
          AND SDate <= CURRENT_DATE;
        
        IF active_users > 0 THEN
            UPDATE EQUIPMENT SET Status = 'In Use' WHERE EID = NEW.EID AND Status != 'Retired';
        ELSE
            UPDATE EQUIPMENT SET Status = 'Available' WHERE EID = NEW.EID AND Status = 'In Use';
        END IF;
    END IF;
    
    -- For DELETE, check the old equipment
    IF TG_OP = 'DELETE' THEN
        SELECT COUNT(*) INTO active_users
        FROM USES
        WHERE EID = OLD.EID
          AND (EDate IS NULL OR EDate >= CURRENT_DATE)
          AND SDate <= CURRENT_DATE;
        
        IF active_users = 0 THEN
            UPDATE EQUIPMENT SET Status = 'Available' WHERE EID = OLD.EID AND Status = 'In Use';
        END IF;
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_equipment_status
AFTER INSERT OR UPDATE OR DELETE ON USES
FOR EACH ROW EXECUTE FUNCTION update_equipment_status();

-- 7. Ensure each lab member works on at least one project (advisory - checked at application level)
-- Note: This constraint is better enforced at application level to allow member creation before project assignment

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- View: All members with their type-specific details
CREATE OR REPLACE VIEW v_member_details AS
SELECT 
    lm.MID,
    lm.Name,
    lm.MType,
    lm.JoinDate,
    f.Department,
    s.SID AS StudentID,
    s.Level,
    s.Major,
    c.Affiliation,
    c.Biography
FROM LAB_MEMBER lm
LEFT JOIN FACULTY f ON lm.MID = f.MID
LEFT JOIN STUDENT s ON lm.MID = s.MID
LEFT JOIN COLLABORATOR c ON lm.MID = c.MID;

-- View: Project details with leader information
CREATE OR REPLACE VIEW v_project_details AS
SELECT 
    p.PID,
    p.Title,
    p.SDate AS StartDate,
    p.EDate AS EndDate,
    p.EDuration AS ExpectedDuration,
    p.Status,
    p.LeaderMID,
    lm.Name AS LeaderName,
    f.Department AS LeaderDepartment
FROM PROJECT p
LEFT JOIN LAB_MEMBER lm ON p.LeaderMID = lm.MID
LEFT JOIN FACULTY f ON p.LeaderMID = f.MID;

-- View: Equipment usage summary
CREATE OR REPLACE VIEW v_equipment_usage AS
SELECT 
    e.EID,
    e.EName,
    e.EType,
    e.Status,
    COUNT(CASE WHEN u.EDate IS NULL OR u.EDate >= CURRENT_DATE THEN 1 END) AS CurrentUsers,
    COUNT(u.MID) AS TotalUsageRecords
FROM EQUIPMENT e
LEFT JOIN USES u ON e.EID = u.EID
GROUP BY e.EID, e.EName, e.EType, e.Status;

-- View: Publication counts per member
CREATE OR REPLACE VIEW v_member_publications AS
SELECT 
    lm.MID,
    lm.Name,
    lm.MType,
    COUNT(p.PubID) AS PublicationCount
FROM LAB_MEMBER lm
LEFT JOIN PUBLISHES p ON lm.MID = p.MID
GROUP BY lm.MID, lm.Name, lm.MType;

-- ============================================
-- UTILITY FUNCTIONS
-- ============================================

-- Function to get active projects count for a member
CREATE OR REPLACE FUNCTION get_active_projects_count(member_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    count INTEGER;
BEGIN
    SELECT COUNT(*) INTO count
    FROM WORKS w
    JOIN PROJECT p ON w.PID = p.PID
    WHERE w.MID = member_id AND p.Status = 'Active';
    RETURN count;
END;
$$ LANGUAGE plpgsql;

-- Function to check if a grant is active
CREATE OR REPLACE FUNCTION is_grant_active(grant_id INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    g_start DATE;
    g_duration INTEGER;
BEGIN
    SELECT StartDate, Duration INTO g_start, g_duration
    FROM GRANT_TABLE WHERE GID = grant_id;
    
    IF g_start IS NULL THEN
        RETURN FALSE;
    END IF;
    
    RETURN CURRENT_DATE BETWEEN g_start AND (g_start + (g_duration || ' months')::INTERVAL);
END;
$$ LANGUAGE plpgsql;

-- Grant appropriate permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_user;

COMMENT ON TABLE LAB_MEMBER IS 'Base table for all lab members (faculty, students, collaborators)';
COMMENT ON TABLE FACULTY IS 'Faculty-specific attributes';
COMMENT ON TABLE STUDENT IS 'Student-specific attributes';
COMMENT ON TABLE COLLABORATOR IS 'External collaborator-specific attributes';
COMMENT ON TABLE PROJECT IS 'Research projects in the lab';
COMMENT ON TABLE GRANT_TABLE IS 'Funding grants (GRANT is reserved word)';
COMMENT ON TABLE EQUIPMENT IS 'Lab equipment inventory';
COMMENT ON TABLE PUBLICATION IS 'Research publications';
COMMENT ON TABLE WORKS IS 'Member-Project assignment relationship';
COMMENT ON TABLE FUNDS IS 'Grant-Project funding relationship';
COMMENT ON TABLE USES IS 'Member-Equipment usage relationship';
COMMENT ON TABLE MENTORS IS 'Mentorship relationships between members';
COMMENT ON TABLE PUBLISHES IS 'Member-Publication authorship relationship';
