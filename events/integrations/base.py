from abc import ABC, abstractmethod


class MessagingIntegration(ABC):
    """Abstract base for messaging integrations.

    Concrete integrations must implement sending and webhook handling.
    """

    @abstractmethod
    def send_message(self, from_, to_number, message):
        """Send a message.

        Args:
            from_ (str): sender number or id
            to_number (str): recipient number
            message (str): message body
        """

    @abstractmethod
    def handle_webhook(self, request) -> tuple:
        """Handle incoming webhook payload (implementation-specific)."""
