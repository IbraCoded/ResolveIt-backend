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
    AWAITING_RESPONSE = "awaiting response"
    ACCEPTED = "accepted"
    PANEL_CREATED = "panel created"
    MEDIATION_IN_PROGRESS = "mediation in progress"
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    
    # added for the opposite party
    REQUESTED = "requested"
    REJECTED = "rejected"

class NotificationType(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
