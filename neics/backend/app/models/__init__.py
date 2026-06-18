"""Aggregate import of all ORM models so metadata is fully registered."""
from app.models.enterprise import (  # noqa: F401
    Enterprise,
    EnterpriseGroup,
    Establishment,
    LegalUnit,
    OwnershipEdge,
)
from app.models.governance import (  # noqa: F401
    AuditEntry,
    Classification,
    QualityResult,
    ReviewItem,
    User,
)
from app.models.reference import (  # noqa: F401
    Codelist,
    InstitutionalSector,
    IsicClass,
    IsicDivision,
    IsicSection,
    LegalForm,
    SizeThreshold,
)
from app.models.rules import (  # noqa: F401
    ClassificationTest,
    MetadataVariable,
    Rule,
    Standard,
    StandardConcept,
)
