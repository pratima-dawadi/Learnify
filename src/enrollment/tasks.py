from celery import shared_task


@shared_task
def after_enrollment_complete(enrolled_at, completed_at):

    time_duration = completed_at - enrolled_at
    print(
        "***************Congratulations!! you have successfully completed the course ********************"
    )
    print(
        f"*******************Time taken to complete the course: {time_duration}*******************"
    )
