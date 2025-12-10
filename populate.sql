-- ============================================
-- RESEARCH LAB MANAGER - SAMPLE DATA
-- PostgreSQL Implementation
-- ============================================

-- Clear existing data (in reverse order of dependencies)
TRUNCATE TABLE PUBLISHES CASCADE;
TRUNCATE TABLE PUBLICATION CASCADE;
TRUNCATE TABLE USES CASCADE;
TRUNCATE TABLE EQUIPMENT CASCADE;
TRUNCATE TABLE MENTORS CASCADE;
TRUNCATE TABLE WORKS CASCADE;
TRUNCATE TABLE FUNDS CASCADE;
TRUNCATE TABLE PROJECT CASCADE;
TRUNCATE TABLE GRANT_TABLE CASCADE;
TRUNCATE TABLE FACULTY CASCADE;
TRUNCATE TABLE STUDENT CASCADE;
TRUNCATE TABLE COLLABORATOR CASCADE;
TRUNCATE TABLE LAB_MEMBER CASCADE;

-- Reset sequences
ALTER SEQUENCE lab_member_mid_seq RESTART WITH 1;
ALTER SEQUENCE grant_table_gid_seq RESTART WITH 1;
ALTER SEQUENCE project_pid_seq RESTART WITH 1;
ALTER SEQUENCE equipment_eid_seq RESTART WITH 1;
ALTER SEQUENCE publication_pubid_seq RESTART WITH 1;

-- ============================================
-- LAB MEMBERS (25 total: 5 Faculty, 15 Students, 5 Collaborators)
-- ============================================

-- Faculty Members (MID 1-5)
INSERT INTO LAB_MEMBER (Name, MType, JoinDate) VALUES
('Dr. Sarah Chen', 'Faculty', '2018-08-15'),
('Dr. Michael Rodriguez', 'Faculty', '2019-01-10'),
('Dr. Emily Watson', 'Faculty', '2020-03-20'),
('Dr. James Park', 'Faculty', '2017-09-01'),
('Dr. Lisa Thompson', 'Faculty', '2021-06-15');

INSERT INTO FACULTY (MID, Department) VALUES
(1, 'Computer Science'),
(2, 'Electrical Engineering'),
(3, 'Computer Science'),
(4, 'Data Science'),
(5, 'Computer Science');

-- Student Members (MID 6-20)
INSERT INTO LAB_MEMBER (Name, MType, JoinDate) VALUES
('Alex Johnson', 'Student', '2022-09-01'),
('Maria Garcia', 'Student', '2021-09-01'),
('David Kim', 'Student', '2023-01-15'),
('Jennifer Lee', 'Student', '2022-01-10'),
('Robert Brown', 'Student', '2021-06-01'),
('Amanda White', 'Student', '2023-09-01'),
('Christopher Davis', 'Student', '2022-06-15'),
('Jessica Martinez', 'Student', '2020-09-01'),
('Daniel Wilson', 'Student', '2023-01-10'),
('Ashley Taylor', 'Student', '2022-09-01'),
('Matthew Anderson', 'Student', '2021-01-15'),
('Nicole Thomas', 'Student', '2023-06-01'),
('Ryan Jackson', 'Student', '2022-01-15'),
('Stephanie Harris', 'Student', '2021-09-01'),
('Kevin Clark', 'Student', '2024-01-10');

INSERT INTO STUDENT (MID, SID, Level, Major) VALUES
(6, 'S2022001', 'Graduate', 'Computer Science'),
(7, 'S2021002', 'Graduate', 'Computer Science'),
(8, 'S2023003', 'Graduate', 'Data Science'),
(9, 'S2022004', 'Graduate', 'Electrical Engineering'),
(10, 'S2021005', 'Senior', 'Computer Science'),
(11, 'S2023006', 'Junior', 'Data Science'),
(12, 'S2022007', 'Graduate', 'Computer Science'),
(13, 'S2020008', 'Graduate', 'Computer Science'),
(14, 'S2023009', 'Senior', 'Electrical Engineering'),
(15, 'S2022010', 'Graduate', 'Data Science'),
(16, 'S2021011', 'Graduate', 'Computer Science'),
(17, 'S2023012', 'Junior', 'Computer Science'),
(18, 'S2022013', 'Graduate', 'Electrical Engineering'),
(19, 'S2021014', 'Graduate', 'Data Science'),
(20, 'S2024015', 'Sophomore', 'Computer Science');

-- Collaborator Members (MID 21-25)
INSERT INTO LAB_MEMBER (Name, MType, JoinDate) VALUES
('Dr. John Smith', 'Collaborator', '2022-03-01'),
('Dr. Rachel Green', 'Collaborator', '2021-11-15'),
('Dr. William Turner', 'Collaborator', '2023-02-20'),
('Dr. Catherine Moore', 'Collaborator', '2022-07-10'),
('Dr. Andrew Phillips', 'Collaborator', '2023-08-01');

INSERT INTO COLLABORATOR (MID, Affiliation, Biography) VALUES
(21, 'MIT - Computer Science Department', 'Expert in machine learning and natural language processing with 15+ years of research experience.'),
(22, 'Stanford University - AI Lab', 'Specializes in computer vision and deep learning architectures.'),
(23, 'Google Research', 'Industry researcher focusing on large-scale distributed systems and cloud computing.'),
(24, 'IBM Research', 'Quantum computing researcher with expertise in quantum algorithms.'),
(25, 'Microsoft Research', 'Human-computer interaction specialist with focus on accessibility.');

-- ============================================
-- GRANTS (8 grants)
-- ============================================

INSERT INTO GRANT_TABLE (Source, Budget, StartDate, Duration) VALUES
('National Science Foundation (NSF)', 500000.00, '2023-01-01', 36),
('Department of Energy (DOE)', 750000.00, '2022-06-01', 48),
('DARPA', 1200000.00, '2023-07-01', 24),
('National Institutes of Health (NIH)', 400000.00, '2024-01-01', 36),
('Army Research Office (ARO)', 600000.00, '2023-03-15', 30),
('Google Research Grant', 250000.00, '2023-09-01', 18),
('Microsoft Academic Grant', 180000.00, '2024-03-01', 24),
('Intel University Partnership', 300000.00, '2022-09-01', 36);

-- ============================================
-- PROJECTS (10 projects)
-- ============================================

INSERT INTO PROJECT (Title, SDate, EDate, EDuration, Status, LeaderMID) VALUES
('Deep Learning for Medical Image Analysis', '2023-02-01', NULL, 24, 'Active', 1),
('Quantum-Resistant Cryptography Implementation', '2022-07-01', '2024-06-30', 24, 'Completed', 2),
('Natural Language Understanding for Accessibility', '2023-08-01', NULL, 18, 'Active', 3),
('Autonomous Drone Navigation System', '2023-04-01', NULL, 30, 'Active', 4),
('Federated Learning Privacy Framework', '2024-01-15', NULL, 24, 'Active', 1),
('IoT Security Protocol Development', '2023-06-01', NULL, 20, 'Paused', 2),
('Computer Vision for Autonomous Vehicles', '2022-09-01', '2024-08-31', 24, 'Completed', 3),
('Explainable AI for Healthcare Decisions', '2024-02-01', NULL, 18, 'Active', 5),
('Edge Computing Optimization', '2023-10-01', NULL, 15, 'Active', 4),
('Blockchain-based Data Integrity System', '2024-04-01', NULL, 24, 'Active', 5);

-- ============================================
-- FUNDS (Grant-Project relationships)
-- ============================================

INSERT INTO FUNDS (GID, PID) VALUES
(1, 1),  -- NSF funds Medical Image Analysis
(1, 5),  -- NSF funds Federated Learning
(2, 2),  -- DOE funds Quantum Cryptography
(2, 6),  -- DOE funds IoT Security
(3, 4),  -- DARPA funds Drone Navigation
(3, 7),  -- DARPA funds Computer Vision
(4, 1),  -- NIH funds Medical Image Analysis
(4, 8),  -- NIH funds Explainable AI
(5, 4),  -- ARO funds Drone Navigation
(6, 3),  -- Google funds NLU Accessibility
(6, 8),  -- Google funds Explainable AI
(7, 10), -- Microsoft funds Blockchain
(8, 9),  -- Intel funds Edge Computing
(8, 6);  -- Intel funds IoT Security

-- ============================================
-- WORKS (Member-Project assignments)
-- ============================================

-- Project 1: Deep Learning for Medical Image Analysis (Leader: Dr. Sarah Chen)
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(1, 1, 'Principal Investigator', 15.0),
(6, 1, 'Research Assistant', 20.0),
(7, 1, 'Research Assistant', 20.0),
(13, 1, 'Senior Research Assistant', 25.0),
(21, 1, 'Advisor', 5.0);

-- Project 2: Quantum-Resistant Cryptography (Leader: Dr. Michael Rodriguez)
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(2, 2, 'Principal Investigator', 12.0),
(9, 2, 'Research Assistant', 20.0),
(18, 2, 'Research Assistant', 18.0),
(24, 2, 'Consultant', 8.0);

-- Project 3: NLU for Accessibility (Leader: Dr. Emily Watson)
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(3, 3, 'Principal Investigator', 15.0),
(8, 3, 'Research Assistant', 22.0),
(12, 3, 'Research Assistant', 20.0),
(25, 3, 'Advisor', 6.0);

-- Project 4: Autonomous Drone Navigation (Leader: Dr. James Park)
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(4, 4, 'Principal Investigator', 18.0),
(10, 4, 'Lead Developer', 25.0),
(14, 4, 'Research Assistant', 20.0),
(16, 4, 'Research Assistant', 15.0);

-- Project 5: Federated Learning Privacy (Leader: Dr. Sarah Chen)
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(1, 5, 'Principal Investigator', 10.0),
(7, 5, 'Lead Researcher', 25.0),
(15, 5, 'Research Assistant', 20.0),
(22, 5, 'Consultant', 5.0);

-- Project 6: IoT Security Protocol (Leader: Dr. Michael Rodriguez) - Paused
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(2, 6, 'Principal Investigator', 8.0),
(9, 6, 'Research Assistant', 15.0),
(11, 6, 'Junior Researcher', 10.0);

-- Project 7: Computer Vision for Autonomous Vehicles (Leader: Dr. Emily Watson) - Completed
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(3, 7, 'Principal Investigator', 15.0),
(13, 7, 'Lead Researcher', 30.0),
(16, 7, 'Research Assistant', 20.0),
(22, 7, 'Advisor', 5.0);

-- Project 8: Explainable AI for Healthcare (Leader: Dr. Lisa Thompson)
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(5, 8, 'Principal Investigator', 20.0),
(6, 8, 'Research Assistant', 15.0),
(8, 8, 'Research Assistant', 18.0),
(19, 8, 'Data Analyst', 22.0);

-- Project 9: Edge Computing Optimization (Leader: Dr. James Park)
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(4, 9, 'Principal Investigator', 12.0),
(10, 9, 'Lead Developer', 20.0),
(17, 9, 'Junior Developer', 15.0),
(23, 9, 'Technical Advisor', 8.0);

-- Project 10: Blockchain Data Integrity (Leader: Dr. Lisa Thompson)
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(5, 10, 'Principal Investigator', 15.0),
(12, 10, 'Research Assistant', 20.0),
(20, 10, 'Junior Researcher', 12.0);

-- Additional cross-project assignments
INSERT INTO WORKS (MID, PID, Role, Hours) VALUES
(13, 5, 'Senior Advisor', 5.0),
(19, 1, 'Data Analyst', 10.0),
(16, 8, 'Research Assistant', 12.0);

-- ============================================
-- EQUIPMENT (15 pieces of equipment)
-- ============================================

INSERT INTO EQUIPMENT (EName, EType, PDate, Status) VALUES
('NVIDIA DGX A100', 'GPU Server', '2022-03-15', 'In Use'),
('Dell PowerEdge R750', 'Server', '2021-06-20', 'In Use'),
('Oscilloscope Keysight DSOX3024T', 'Measurement', '2020-09-10', 'Available'),
('DJI Matrice 300 RTK', 'Drone', '2023-01-25', 'In Use'),
('Intel RealSense D455', 'Camera', '2022-11-30', 'Available'),
('Quantum Development Kit', 'Quantum Computing', '2023-05-15', 'In Use'),
('3D Printer Ultimaker S5', 'Manufacturing', '2021-04-10', 'Available'),
('NVIDIA Jetson AGX Orin', 'Edge Computing', '2023-08-20', 'In Use'),
('Logic Analyzer Saleae Pro 16', 'Measurement', '2020-02-28', 'Available'),
('AWS DeepRacer', 'Robotics', '2022-07-15', 'In Use'),
('Raspberry Pi Cluster (10 units)', 'Computing', '2021-11-05', 'Available'),
('Intel NUC 12 Pro', 'Edge Computing', '2023-03-10', 'Available'),
('Thermal Camera FLIR E8-XT', 'Measurement', '2022-01-20', 'Retired'),
('LiDAR Velodyne VLP-16', 'Sensor', '2022-05-30', 'In Use'),
('Network Analyzer Keysight N5242B', 'Measurement', '2021-08-15', 'Available');

-- ============================================
-- USES (Equipment usage records)
-- ============================================

-- Current active usage
INSERT INTO USES (MID, EID, SDate, EDate, Purpose) VALUES
(6, 1, '2024-01-15', NULL, 'Training deep learning models for medical image analysis'),
(7, 1, '2024-02-01', NULL, 'Running federated learning experiments'),
(13, 1, '2024-01-20', NULL, 'Computer vision model training'),
(9, 2, '2024-03-01', NULL, 'Quantum cryptography simulations'),
(10, 4, '2024-02-15', NULL, 'Drone navigation testing'),
(14, 4, '2024-03-10', NULL, 'Autonomous flight experiments'),
(2, 6, '2024-01-05', NULL, 'Quantum algorithm development'),
(24, 6, '2024-02-20', NULL, 'Quantum computing research'),
(4, 8, '2024-04-01', NULL, 'Edge computing optimization tests'),
(17, 8, '2024-04-15', NULL, 'Edge device programming'),
(10, 10, '2024-03-20', NULL, 'Reinforcement learning experiments'),
(16, 14, '2024-02-28', NULL, 'LiDAR data collection for autonomous vehicles');

-- Historical usage (completed)
INSERT INTO USES (MID, EID, SDate, EDate, Purpose) VALUES
(13, 1, '2023-06-01', '2023-12-31', 'Previous deep learning project'),
(3, 2, '2023-01-15', '2023-08-30', 'Computer vision server tasks'),
(16, 4, '2023-09-01', '2023-12-15', 'Initial drone testing'),
(18, 6, '2023-07-01', '2023-11-30', 'Quantum algorithm testing'),
(10, 10, '2023-05-15', '2023-10-30', 'Robotics experiments'),
(8, 5, '2023-11-01', '2024-02-28', 'Camera testing for accessibility project'),
(12, 7, '2023-08-01', '2023-12-15', '3D printing prototypes'),
(6, 1, '2023-03-01', '2023-12-31', 'Initial medical imaging experiments');

-- ============================================
-- MENTORSHIP RELATIONS
-- ============================================

INSERT INTO MENTORS (MentorMID, MenteeMID, StartDate, EndDate) VALUES
-- Faculty mentoring students
(1, 6, '2022-09-15', NULL),   -- Dr. Chen mentors Alex
(1, 7, '2021-09-15', NULL),   -- Dr. Chen mentors Maria
(2, 9, '2022-02-01', NULL),   -- Dr. Rodriguez mentors Jennifer
(2, 18, '2022-07-01', NULL),  -- Dr. Rodriguez mentors Ryan
(3, 8, '2023-02-01', NULL),   -- Dr. Watson mentors David
(3, 12, '2022-07-01', NULL),  -- Dr. Watson mentors Christopher
(4, 10, '2021-06-15', NULL),  -- Dr. Park mentors Robert
(4, 14, '2023-02-01', NULL),  -- Dr. Park mentors Daniel
(4, 16, '2021-02-01', NULL),  -- Dr. Park mentors Matthew
(5, 19, '2021-10-01', NULL),  -- Dr. Thompson mentors Stephanie
(5, 15, '2022-10-01', NULL),  -- Dr. Thompson mentors Ashley

-- Senior students mentoring junior students
(13, 11, '2023-10-01', NULL), -- Jessica mentors Amanda
(7, 17, '2023-07-01', NULL),  -- Maria mentors Nicole
(10, 20, '2024-02-01', NULL), -- Robert mentors Kevin

-- Completed mentorships
(1, 13, '2020-09-15', '2023-08-31'), -- Dr. Chen mentored Jessica (graduated)
(3, 16, '2021-02-01', '2023-05-31'); -- Dr. Watson mentored Matthew (changed advisor)

-- ============================================
-- PUBLICATIONS (20 publications)
-- ============================================

INSERT INTO PUBLICATION (Title, PubDate, Venue, DOI) VALUES
('Deep Learning Approaches for Medical Image Segmentation: A Comprehensive Survey', '2024-03-15', 'IEEE Transactions on Medical Imaging', '10.1109/TMI.2024.001234'),
('Quantum-Resistant Lattice-Based Cryptographic Protocols', '2024-01-20', 'ACM Conference on Computer and Communications Security', '10.1145/3576915.001'),
('Accessible Natural Language Interfaces for Visually Impaired Users', '2024-02-28', 'CHI Conference on Human Factors in Computing Systems', '10.1145/3544548.001'),
('Autonomous Navigation in GPS-Denied Environments Using Visual SLAM', '2023-11-10', 'IEEE International Conference on Robotics and Automation', '10.1109/ICRA.2023.001'),
('Privacy-Preserving Federated Learning: Challenges and Solutions', '2024-04-05', 'Nature Machine Intelligence', '10.1038/s42256-024-001'),
('IoT Security Framework for Smart City Infrastructure', '2023-08-22', 'IEEE Internet of Things Journal', '10.1109/JIOT.2023.001'),
('Real-Time Object Detection for Autonomous Vehicles', '2023-12-15', 'IEEE Conference on Computer Vision and Pattern Recognition', '10.1109/CVPR.2023.001'),
('Explainable AI in Clinical Decision Support Systems', '2024-05-10', 'Journal of Biomedical Informatics', '10.1016/j.jbi.2024.001'),
('Edge Computing Optimization for Real-Time Applications', '2024-03-28', 'IEEE Transactions on Cloud Computing', '10.1109/TCC.2024.001'),
('Blockchain-Based Data Provenance in Healthcare', '2024-04-18', 'Journal of Medical Internet Research', '10.2196/jmir.2024.001'),
('Transfer Learning for Medical Image Classification', '2023-09-30', 'Medical Image Analysis', '10.1016/j.media.2023.001'),
('Post-Quantum Cryptography: Implementation Challenges', '2023-10-15', 'IEEE Security and Privacy', '10.1109/SP.2023.001'),
('Speech Recognition for Accessibility Applications', '2024-01-08', 'ACM SIGACCESS Conference on Computers and Accessibility', '10.1145/3597638.001'),
('Multi-Robot Coordination for Search and Rescue', '2023-07-20', 'Autonomous Robots', '10.1007/s10514-023-001'),
('Differential Privacy in Machine Learning Pipelines', '2024-02-14', 'AAAI Conference on Artificial Intelligence', '10.1609/aaai.2024.001'),
('Secure Communication Protocols for IoT Devices', '2023-06-25', 'ACM Computing Surveys', '10.1145/3582016.001'),
('3D Reconstruction from Monocular Video', '2024-04-22', 'International Journal of Computer Vision', '10.1007/s11263-024-001'),
('Machine Learning for Drug Discovery: A Review', '2024-03-01', 'Briefings in Bioinformatics', '10.1093/bib/2024.001'),
('Efficient Neural Network Architectures for Edge Devices', '2024-05-05', 'IEEE Transactions on Neural Networks', '10.1109/TNNLS.2024.001'),
('Consensus Mechanisms in Distributed Systems', '2024-04-30', 'ACM Computing Surveys', '10.1145/3609027.001');

-- ============================================
-- PUBLISHES (Author-Publication relationships)
-- ============================================

-- Publication 1: Deep Learning Medical Image
INSERT INTO PUBLISHES (MID, PubID) VALUES (1, 1), (6, 1), (13, 1), (21, 1);

-- Publication 2: Quantum Cryptography
INSERT INTO PUBLISHES (MID, PubID) VALUES (2, 2), (9, 2), (18, 2), (24, 2);

-- Publication 3: NLU Accessibility
INSERT INTO PUBLISHES (MID, PubID) VALUES (3, 3), (8, 3), (25, 3);

-- Publication 4: Autonomous Navigation
INSERT INTO PUBLISHES (MID, PubID) VALUES (4, 4), (10, 4), (14, 4);

-- Publication 5: Federated Learning Privacy
INSERT INTO PUBLISHES (MID, PubID) VALUES (1, 5), (7, 5), (15, 5), (22, 5);

-- Publication 6: IoT Security
INSERT INTO PUBLISHES (MID, PubID) VALUES (2, 6), (9, 6), (11, 6);

-- Publication 7: Computer Vision Autonomous Vehicles
INSERT INTO PUBLISHES (MID, PubID) VALUES (3, 7), (13, 7), (16, 7), (22, 7);

-- Publication 8: Explainable AI Healthcare
INSERT INTO PUBLISHES (MID, PubID) VALUES (5, 8), (6, 8), (8, 8), (19, 8);

-- Publication 9: Edge Computing
INSERT INTO PUBLISHES (MID, PubID) VALUES (4, 9), (10, 9), (17, 9), (23, 9);

-- Publication 10: Blockchain Healthcare
INSERT INTO PUBLISHES (MID, PubID) VALUES (5, 10), (12, 10);

-- Publication 11: Transfer Learning Medical
INSERT INTO PUBLISHES (MID, PubID) VALUES (1, 11), (7, 11), (13, 11);

-- Publication 12: Post-Quantum Crypto
INSERT INTO PUBLISHES (MID, PubID) VALUES (2, 12), (18, 12), (24, 12);

-- Publication 13: Speech Recognition Accessibility
INSERT INTO PUBLISHES (MID, PubID) VALUES (3, 13), (12, 13), (25, 13);

-- Publication 14: Multi-Robot Coordination
INSERT INTO PUBLISHES (MID, PubID) VALUES (4, 14), (14, 14), (16, 14);

-- Publication 15: Differential Privacy ML
INSERT INTO PUBLISHES (MID, PubID) VALUES (1, 15), (7, 15), (22, 15);

-- Publication 16: Secure IoT Communication
INSERT INTO PUBLISHES (MID, PubID) VALUES (2, 16), (9, 16);

-- Publication 17: 3D Reconstruction
INSERT INTO PUBLISHES (MID, PubID) VALUES (3, 17), (13, 17), (16, 17);

-- Publication 18: ML Drug Discovery
INSERT INTO PUBLISHES (MID, PubID) VALUES (5, 18), (19, 18), (21, 18);

-- Publication 19: Efficient Neural Networks Edge
INSERT INTO PUBLISHES (MID, PubID) VALUES (4, 19), (10, 19), (17, 19), (23, 19);

-- Publication 20: Consensus Distributed Systems
INSERT INTO PUBLISHES (MID, PubID) VALUES (5, 20), (12, 20), (20, 20);

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Uncomment these to verify data after insertion:
-- SELECT 'LAB_MEMBER' AS table_name, COUNT(*) AS count FROM LAB_MEMBER
-- UNION ALL SELECT 'FACULTY', COUNT(*) FROM FACULTY
-- UNION ALL SELECT 'STUDENT', COUNT(*) FROM STUDENT
-- UNION ALL SELECT 'COLLABORATOR', COUNT(*) FROM COLLABORATOR
-- UNION ALL SELECT 'GRANT_TABLE', COUNT(*) FROM GRANT_TABLE
-- UNION ALL SELECT 'PROJECT', COUNT(*) FROM PROJECT
-- UNION ALL SELECT 'FUNDS', COUNT(*) FROM FUNDS
-- UNION ALL SELECT 'WORKS', COUNT(*) FROM WORKS
-- UNION ALL SELECT 'MENTORS', COUNT(*) FROM MENTORS
-- UNION ALL SELECT 'EQUIPMENT', COUNT(*) FROM EQUIPMENT
-- UNION ALL SELECT 'USES', COUNT(*) FROM USES
-- UNION ALL SELECT 'PUBLICATION', COUNT(*) FROM PUBLICATION
-- UNION ALL SELECT 'PUBLISHES', COUNT(*) FROM PUBLISHES;
