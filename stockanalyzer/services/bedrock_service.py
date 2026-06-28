import json
import boto3

from config.settings import settings
from config.logging_config import logger


class BedrockService:

    def __init__(self):

        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region
        )

        logger.info(
            f"Bedrock initialized. Region={settings.aws_region}, Model={settings.bedrock_model_id}"
        )

    def chat(self, prompt: str) -> str:
        """
        Invoke Amazon Bedrock Nova Lite model.

        Returns plain text.
        """

        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "temperature": 0.2,
                "maxTokens": 2048,
                "topP": 0.9
            }
        }

        try:

            response = self.client.invoke_model(
                modelId=settings.bedrock_model_id,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json"
            )

            response_body = json.loads(
                response["body"].read()
            )

            logger.debug(response_body)

            output = response_body.get("output", {})

            message = output.get("message", {})

            content = message.get("content", [])

            if not content:
                return ""

            return content[0].get("text", "").strip()

        except Exception as ex:

            logger.exception("Bedrock invocation failed")

            raise ex


bedrock_service = BedrockService()