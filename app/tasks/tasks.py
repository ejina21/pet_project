from app.config import settings
from app.tasks.celery_config import celery
from PIL import Image
from pathlib import Path
from pydantic import EmailStr
import smtplib
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(path: str):
    img_path = Path(path)
    img = Image.open(img_path)
    img_resized_1000_500 = img.resize((1000, 500))
    img_resized_200_100 = img.resize((200, 100))
    img_resized_1000_500.save(f"app/static/images/resized_1000_500_{img_path.name}")
    img_resized_200_100.save(f"app/static/images/resized_200_100_{img_path.name}")


@celery.task(bind=True, default_retry_delay=300, max_retries=5)
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    msg_content = create_booking_confirmation_template(
        booking=booking, email_to=email_to
    )
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
