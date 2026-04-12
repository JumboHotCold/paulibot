"""
Mock data for PauliBot MVP.
Stores immutable university information to ensure reliability (Rule 2).
"""

LOCATIONS = {
    "library": {
        "name": "SPUS University Library",
        "description": "The main hub for research and study, located on the 2nd floor of the Main Building.",
        "map_available": True
    },
    "registrar": {
        "name": "Registrar's Office",
        "description": "Handles student records, enrollment, and grades. Located at the Ground Floor, Admin Building.",
        "map_available": True
    },
    "canteen": {
        "name": "University Canteen",
        "description": "Offers various meals and snacks for students and staff. Located near the gym.",
        "map_available": True
    },
    "finance": {
        "name": "Finance Office",
        "description": "For tuition payment and financial inquiries. Ground Floor, Admin Building.",
        "map_available": True
    },
    "clinic": {
        "name": "University Clinic",
        "description": "Provides basic medical handling. Located near the Guidance Office.",
        "map_available": True
    },
     "guidance": {
        "name": "Guidance Office",
        "description": "Provides counseling and career guidance. 2nd Floor, Admin Building.",
        "map_available": True
    }
}

STAFF = {
    "president": {
        "name": "Sr. Marie Rosanne Mallillin, SPC",
        "position": "University President",
        "office": "President's Office, 2nd Floor Admin Building"
    },
    "vp_academics": {
        "name": "Dr. Antonio Talamera",
        "position": "VP for Academics",
        "office": "VPA Office, 2nd Floor Admin Building"
    },
    "dean_cics": {
        "name": "Mr. Nikko Ederio",
        "position": "Dean, College of Information and Computing Sciences",
        "office": "CICS Faculty Room, 3rd Floor IT Building"
    }
}

FAQS = [
    {
        "category": "Admissions",
        "question": "How do I enroll in Grade 7?",
        "answer": "To enroll, visit www.spus.edu.ph and click on the 'Admission' tab, or visit the Registrar's Office. For incoming Grade 7, the requirements are: Original Report Card, Original PSA Birth Certificate, 2 pcs. 2x2 ID Picture, and Original Good Moral Certificate. For parents, a BIR-ITR or Brgy. Certificate of Indigency is needed. Good news: There are 350 ESC Slots available!"
    },
    {
        "category": "Admissions",
        "question": "What are the requirements for Nursery, Kindergarten, and Grade 1?",
        "answer": "The requirements for incoming Nursery, Kindergarten, and Grade 1 pupils are: Original PSA Birth Certificate, 2 pcs 2x2 ID Picture, 250.00 Php Admission Test Fee, and 3,000.00 Php Enrollment Fee."
    },
    {
        "category": "Admissions",
        "question": "What are the requirements for incoming Grade 11 (SHS)?",
        "answer": "Requirements include: Original Report Card, Original PSA Birth Certificate, 2 pcs. 2x2 ID Picture, Original Good Moral Certificate, and an ESC Certificate (only for completers from Private Schools). For the SHS Voucher Program Subsidy, Public School Completers are automatically eligible, while Private School Completers need to present their ESC Certificate to qualify."
    },
    {
        "category": "Tuition and Finance",
        "question": "How much is the tuition?",
        "answer": "Tuition fees vary depending on the program and year level. Please visit the Finance Office located at the Ground Floor, Admin Building for a detailed and accurate assessment."
    },
    {
        "category": "Scholarships",
        "question": "Are there scholarships available?",
        "answer": "Yes! SPUS offers 350 ESC Slots for incoming Grade 7 students. We also support the SHS Voucher Program Subsidy for incoming Grade 11 students (automatically eligible for public school completers, ESC certificate required for private school completers). For other academic and athletic scholarships, visit the Guidance Office for application details."
    },
    {
        "category": "Academics",
        "question": "What college courses are available?",
        "answer": "SPUS offers a comprehensive range of undergraduate programs across several colleges:\n- College of Health Sciences: BS Nursing, BS Psychology.\n- College of Education, Arts and Sciences: BA (Political Science, Philosophy, English Language, Sociology, Mass Comm), BS Mathematics, BS Public Administration, Bachelor of Elementary/Secondary/Early Childhood/Physical Education.\n- College of Business Management and Accountancy: BS Accountancy, BS Business Administration, BS Hospitality/Tourism Management, BS Accounting IS, BS Office Admin.\n- College of Engineering & IT: BS Mining/Civil/Computer Engineering, BS IT.\n- College of Criminal Justice Education: BS Criminology, Bachelor of Forensic Science."
    },
    {
        "category": "Academics",
        "question": "Does SPUS offer Graduate School programs?",
        "answer": "Yes, SPUS Graduate School and Professional Studies (GSPS) offers PhDs in Educational Management and Business & Management. We also offer Master's degrees in Business Administration (MBA), Public Administration (MPA), Nursing (MSN, MAN), Science Teaching, Math Teaching, English, Filipino, Home Economics, Cultural Education, and Curriculum Development & Design. For inquiries, you may email gsps@spus.edu.ph or contact Ma. Lourdes O. Saguran at 09123456789."
    },
    {
        "category": "Academics",
        "question": "Why choose SPUS?",
        "answer": "Choosing SPUS means embracing:\n- Faith-Based Education: Integrating Catholic Christian values forming ethically grounded leaders.\n- Academic Excellence: An Outcomes-Based Education (OBE) framework ensuring rigorous, industry-relevant skills.\n- Vibrant Campus Life: Diverse student organizations and dynamic campus events.\n- Global Alumni Network: A vast and interconnected network offering mentorship and lifelong support."
    },
    {
        "category": "TVET",
        "question": "What TVET programs are offered?",
        "answer": "SPUS TVET offers Registered Training Center Programs (Diplomas in Health Services, IT, and Hotel & Restaurant Technology; NC II in Computer Systems Servicing, Food & Bev Services, Housekeeping) and Accredited Assessment Center Programs (NC II in Bookkeeping, Computer Systems Servicing, Food & Bev, Housekeeping, Massage Therapy, Hilot Wellness). For inquiries, email tvet@spus.edu.ph or contact Mrs. Chrizely M. Dalagan at 09635606094 / Mrs. Margeorhey B. Mordeno at 09129896596."
    },
    {
        "category": "About SPUS",
        "question": "What is the SPUS Webometrics Ranking?",
        "answer": "SPUS shows a continuous climb in the Webometrics Rankings! For 2026, we are ranked 187th among Philippine HEIs (up from 203rd in 2025 and 212th in 2024), Top 30 in Mindanao, and #5 in the Caraga Region. This reflects our commitment to continuous improvement and academic excellence."
    },
    {
        "category": "About SPUS",
        "question": "What is the university's Vision and Mission?",
        "answer": "VISION: Empowered Paulinians making a difference for Church and society. \nMISSION: Proclaim the Good News enabling Paulinians to reach their full potential through Transformative Formation, Tranquil-daring Innovations, and All-to-all Service."
    },
    {
        "category": "About SPUS",
        "question": "What are the Paulinian Core Values?",
        "answer": "The Paulinian Core Values are:\n- Charism: Developing talents to serve the community.\n- Christ-Centered: Living a life following and imitating Christ.\n- Commission: Having a life purpose to spread the Good News and positively impact the world.\n- Community: Being a responsible citizen prioritizing justice, peace, and environmental protection.\n- Charity: Being warm, hospitable, and 'all to all', especially to the underprivileged."
    },
    {
        "category": "About SPUS",
        "question": "What is the history of SPUS?",
        "answer": "St. Paul University Surigao traces its roots to 1906, initiated by Spanish Benedictine Missionaries. It is a private, Catholic basic and higher education institution run by the Sisters of St. Paul of Chartres (SPC) in Surigao City. It is the first university in the Caraga region, the center for development in teacher education, and the regional center for Gender and Development."
    },
    {
        "category": "About SPUS",
        "question": "What is the SPUS Quality Policy?",
        "answer": "St. Paul University Surigao is committed to delivering quality, Filipino, Catholic Paulinian education that is learner-focused and outcomes-based. This is rooted in a culture of compassionate care through: Holistic formation, constant development of human resources and facilities, active stakeholder involvement in the quality management system, and strict compliance with statutory and accreditation standards."
    },
    {
        "category": "About SPUS",
        "question": "What is the university's Data Privacy Policy?",
        "answer": "SPUS is fully committed to protecting the privacy and personal data of its students, faculty, and staff. Information is collected solely for lawful and legitimate purposes (admissions, academic services, security, research) and won't be sold or shared without consent. All data is protected via strict technical and organizational measures in compliance with applicable data protection laws. Individuals have the right to access, update, or request deletion of their info through the Data Privacy Officer (DPO)."
    },
    {
        "category": "Location",
        "question": "Where is the register?",
        "answer": "The Registrar's Office is located at the Ground Floor of the Admin Building. They handle student records, enrollment processes, and releasing of grades."
    },
    {
        "category": "Location",
        "question": "Where is the registrar office?",
        "answer": "The Registrar's Office is located at the Ground Floor of the Admin Building. Here you can process your enrollment, request records, and check your grades."
    }
]
