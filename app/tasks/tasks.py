import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.logger import logger
from app.tasks.celery_config import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(path: str):
    img_path = Path(path)
    img = Image.open(img_path)
    for width, height in [
        (1000, 500),
        (200, 100)
    ]:
        resized_img = img.resize(size=(width, height))
        resized_img.save(f"app/static/images/resized_{width}_{height}_{img_path.name}")


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
    logger.info(f"Successfully send email message to {email_to}")