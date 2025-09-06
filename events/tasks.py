from celery import shared_task


@shared_task(queue="ai-postprocessing")
def postprocessing(*args, **kwargs):
    print("Postprocessing task executed with args:", args, "and kwargs:", kwargs)
