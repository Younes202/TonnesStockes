"""import httpx
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv(".env")

# Get API key and sandbox domain from environment variables
api_key = os.getenv('MAILGUN_API_KEY')
sandbox_domain = os.getenv('SANDBOX_DOMAIN')
mailgun_url = f"https://api.mailgun.net/v3/{sandbox_domain}/messages"


async def send_email(recipient: str, subject: str, body: str):
    async with httpx.AsyncClient(auth=("api", api_key)) as client:
        response = await client.post(
            mailgun_url,
            data={
                "from": "murichesys@gmail.com",
                "to": recipient,
                "subject": subject,
                "text": body
            }
        )
        if response.status_code != 200:
            error_message = f"Failed to send email. Status code: {response.status_code}, Response: {response.text}"
            logger.error(error_message)  # Log the error
            raise Exception(error_message)
        else:
            logger.info("Email sent successfully")
"""