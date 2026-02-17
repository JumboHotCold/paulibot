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

ADMISSIONS_FAQ = {
    "enrollment": "To enroll, visit the Registrar's Office or go to the online portal at spus.edu.ph/enroll. Requirements include Form 138, Good Moral Certificate, and PSA Birth Certificate.",
    "tuition": "Tuition fees vary by program. Please visit the Finance Office for a detailed assessment.",
    "scholarship": "SPUS offers academic and athletic scholarships. Visit the Guidance Office for application details.",
    "courses": "SPUS offers programs in Engineering, Nursing, Teacher Education, Business, and Computer Studies."
}
