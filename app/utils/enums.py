from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class CaseType(str, Enum):
    FAMILY = "family"
    BUSINESS = "business"
    CRIMINAL = "criminal"

class CaseStatus(str, Enum):
    REGISTERED = "registered"
    AWAITING_RESPONSE = "awaiting_response"
    ACCEPTED = "accepted"
    PANEL_CREATED = "panel_created"
    MEDIATION_IN_PROGRESS = "mediation_in_progress"
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    
    # added for the opposite party
    REQUESTED = "requested"