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
    def get_props(self, request) -> tuple:
        """Extract properties from incoming webhook request.

        Args:
            request: incoming HTTP request

        Returns:
            tuple: (to, from_, message)
        """

    @abstractmethod
    def verify_webhook_token(self, request):
        """Verify webhook token (implementation-specific)."""
