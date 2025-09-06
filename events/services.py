from celery import Celery


class EventService:
    def __init__(self):
        self.celery_client = Celery("maestro")

    def handle_webhook(self, request):
        print(f"Processing event: {request}")

        if request.method == "POST":
            result = self.celery_client.send_task(
                "executor.tasks.run",
                queue="toprocess",
                kwargs={
                    "to": request.POST.get("To"),
                    "from_": request.POST.get("From"),
                    "input": request.POST.get("Body"),
                },
            )

            print(f"Enviando mensagem via WhatsApp: {result}")
