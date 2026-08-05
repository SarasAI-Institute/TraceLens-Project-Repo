"""In-memory storage for TraceLens

This module provides simple in-memory storage for projects and traces.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Project, Trace


class Storage:
    def __init__(self):
        self._projects: Dict[str, Project] = {}
        self._traces: Dict[str, Trace] = {}

    # ============== Project Operations ==============

    def create_project(self, project: Project) -> Project:
        self._projects[project.id] = project
        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        return self._projects.get(project_id)

    def get_all_projects(self) -> List[Project]:
        return list(self._projects.values())

    def update_project(self, project_id: str, project: Project) -> Optional[Project]:
        if project_id not in self._projects:
            return None
        self._projects[project_id] = project
        return project

    def delete_project(self, project_id: str) -> bool:
        if project_id in self._projects:
            del self._projects[project_id]
            return True
        return False

    # ============== Trace Operations ==============

    def create_trace(self, trace: Trace) -> Trace:
        self._traces[trace.id] = trace
        return trace

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        return self._traces.get(trace_id)

    def get_all_traces(self) -> List[Trace]:
        return list(self._traces.values())

    def delete_trace(self, trace_id: str) -> bool:
        if trace_id in self._traces:
            del self._traces[trace_id]
            return True
        return False

    def get_traces_by_project(self, project_id: str) -> List[Trace]:
        return [t for t in self._traces.values() if t.project_id == project_id]

    # ============== Utility ==============

    def clear(self):
        self._projects.clear()
        self._traces.clear()


# Global storage instance
storage = Storage()
