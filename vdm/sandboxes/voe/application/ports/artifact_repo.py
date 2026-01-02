"""
Artifact repository port - interface for artifact storage
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Optional, Union


class ArtifactRepoPort(ABC):
    """
    Abstract interface for artifact storage and retrieval
    """

    @abstractmethod
    async def store_artifact(
        self, candidate_id: str, artifact_type: str, content: Union[str, bytes]
    ) -> str:
        """
        Store an artifact

        Args:
            candidate_id: UUID of candidate
            artifact_type: Type identifier (e.g., "logs", "receipts")
            content: Artifact content

        Returns:
            URI to stored artifact
        """
        pass

    @abstractmethod
    async def get_artifact(self, candidate_id: str, artifact_type: str) -> Optional[bytes]:
        """
        Retrieve an artifact

        Args:
            candidate_id: UUID of candidate
            artifact_type: Type identifier

        Returns:
            Artifact content if found, None otherwise
        """
        pass

    @abstractmethod
    async def export_bundle(self, candidate_id: str, output_path: Path) -> None:
        """
        Export complete artifact bundle as tarball

        Args:
            candidate_id: UUID of candidate
            output_path: Path for output tarball
        """
        pass

    @abstractmethod
    async def cleanup(self, candidate_id: str, keep_receipts: bool = True) -> None:
        """
        Clean up artifacts for a candidate

        Args:
            candidate_id: UUID of candidate
            keep_receipts: If True, preserve receipts
        """
        pass
