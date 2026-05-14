from pydantic import BaseModel, Field
from typing import Optional


# ── Request models ────────────────────────────────────────────────────────────

class AIGenerateRequest(BaseModel):
    """Petición para generar tarjetas mediante IA a partir de texto libre."""
    text: str = Field(
        ...,
        min_length=10,
        description="Texto libre del que la IA extraerá las tarjetas de Jira",
        examples=["Necesitamos crear un módulo de login con OAuth2, "
                  "también hay un bug en el formulario de registro y "
                  "una mejora en el dashboard de métricas."]
    )
    project_key: Optional[str] = Field(
        default=None,
        description="Clave del proyecto Jira. Si no se indica, se usa la del config."
    )


class ManualIssueRequest(BaseModel):
    """Petición para crear una tarjeta en Jira de forma manual, sin IA."""
    summary: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Título de la tarjeta"
    )
    description: Optional[str] = Field(
        default=None,
        description="Descripción detallada de la tarjeta"
    )
    issue_type: Optional[str] = Field(
        default=None,
        description="Tipo de issue: Task, Bug, Story, Epic. "
                    "Si no se indica, se usa el del config."
    )
    priority: Optional[str] = Field(
        default=None,
        description="Prioridad: Highest, High, Medium, Low, Lowest. "
                    "Si no se indica, se usa la del config."
    )
    labels: Optional[list[str]] = Field(
        default_factory=list,
        description="Lista de etiquetas"
    )
    story_points: Optional[int] = Field(
        default=None,
        ge=1,
        le=100,
        description="Story points estimados"
    )
    project_key: Optional[str] = Field(
        default=None,
        description="Clave del proyecto Jira. Si no se indica, se usa la del config."
    )


# ── Response models ───────────────────────────────────────────────────────────

class CreatedIssue(BaseModel):
    """Representa una tarjeta creada en Jira."""
    key: str = Field(description="Clave de la tarjeta, ej: PROJ-42")
    summary: str
    issue_type: str
    priority: str
    url: str = Field(description="URL directa a la tarjeta en Jira")


class AIGenerateResponse(BaseModel):
    """Respuesta de la generación de tarjetas mediante IA."""
    total_issues_created: int
    issues: list[CreatedIssue]
    raw_ai_response: Optional[str] = Field(
        default=None,
        description="Respuesta JSON cruda de la IA (útil para debug)"
    )


class ManualIssueResponse(BaseModel):
    """Respuesta de la creación manual de una tarjeta."""
    issue: CreatedIssue
    message: str = "Tarjeta creada correctamente"
