from typing import Any, Dict, Optional, Protocol


class DatabaseAdapter(Protocol):
    def create(self, collection: str, document: Dict[str, Any]) -> Any:
        ...

    def read(self, collection: str, filter: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        ...

    def update(
        self, collection: str, filter: Dict[str, Any], update: Dict[str, Any]
    ) -> None:
        ...

    def delete(self, collection: str, filter: Dict[str, Any]) -> None:
        ...
