from jira import JIRA
from jira.exceptions import JIRAError
from config import Settings
from models import CreatedIssue
import logging

logger = logging.getLogger(__name__)

class JiraService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = JIRA(
            server=settings.JIRA_URL,
            basic_auth=(settings.JIRA_USER_EMAIL, settings.JIRA_API_TOKEN)
        )

    def create_issue(
        self,
        summary: str,
        description: str = "",
        project_key: str | None = None,
    ) -> CreatedIssue:
        """
        Crea una tarjeta en Jira con solo summary y description.
        """
        project = project_key or self.settings.JIRA_PROJECT_KEY

        issue_dict: dict = {
            "project": {"key": project},
            "summary": summary,
            "description": description,
            "issuetype": {"name": self.settings.JIRA_DEFAULT_ISSUE_TYPE}
        }

        try:
            new_issue = self.client.create_issue(fields=issue_dict)
            logger.info("✅ Issue creada: %s", new_issue.key)
        except JIRAError as exc:
            logger.error("❌ Error al crear issue en Jira: %s", exc.text)
            raise

        return CreatedIssue(
            key=new_issue.key,
            summary=summary,
            issue_type=self.settings.JIRA_DEFAULT_ISSUE_TYPE,
            priority=self.settings.JIRA_DEFAULT_PRIORITY,
            url=f"{self.settings.JIRA_URL}/browse/{new_issue.key}",
        )

    def create_issues_bulk(
        self,
        issues_data: list[dict],
        project_key: str | None = None,
    ) -> list[CreatedIssue]:
        """
        Crea múltiples tarjetas a partir de una lista de dicts.
        Solo usa summary y description.
        """
        created = []
        for issue_data in issues_data:
            created_issue = self.create_issue(
                summary=issue_data.get("summary", "Sin título"),
                description=issue_data.get("description", ""),
                project_key=project_key
            )
            created.append(created_issue)
        return created
