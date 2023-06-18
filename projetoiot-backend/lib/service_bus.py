import os
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage

SERVICE_BUS_CONNECTION = os.environ["SERVICE_BUS_CONNECTION"]
SERVICE_BUS_QUEUE_NAME = os.environ["SERVICE_BUS_QUEUE_NAME"]


async def send_message_to_log_queue(message):
    async with ServiceBusClient.from_connection_string(SERVICE_BUS_CONNECTION) as client:
        sender = client.get_queue_sender(SERVICE_BUS_QUEUE_NAME)
        async with sender:
            message = ServiceBusMessage(message)
            await sender.send_messages(message)
