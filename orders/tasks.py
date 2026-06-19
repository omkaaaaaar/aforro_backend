from celery import shared_task


@shared_task
def order_confirmation_task(
    order_id
):

    print(
        f"Order {order_id} "
        f"confirmed asynchronously"
    )

    return (
        f"Order {order_id} processed"
    )