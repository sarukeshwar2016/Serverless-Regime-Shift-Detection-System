"""
Base adapter interface for all data source adapters.
All adapters (Binance, Stripe, etc.) inherit from this class.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generator


class BaseAdapter(ABC):
    """Abstract base class for all financial data source adapters."""

    def __init__(self, name: str):
        self.name = name
        self.is_connected = False

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the data source."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to the data source."""
        pass

    @abstractmethod
    def stream(self) -> Generator[Dict[str, Any], None, None]:
        """Yield data records from the source as a generator."""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} connected={self.is_connected}>"
