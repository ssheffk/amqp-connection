import pika
import ssl
from pika.credentials import ExternalCredentials

host = 'your_host'
port = 'your_port'
virtual_host = 'your_virtual_host' # staging || production

client_cert_path = 'path_to_client_certificate'
client_key_path = 'path_to_client_key'
ca_cert_path = 'path_to_ca_certificate'

credentials = ExternalCredentials()

# Create a new SSL context for the client-side connection
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(ca_cert_path)
ssl_context.verify_mode = ssl.CERT_REQUIRED


# Load the client certificate and key into the SSL context
ssl_context.load_cert_chain(certfile=client_cert_path, keyfile=client_key_path)

ssl_options = pika.SSLOptions(ssl_context)

parameters = pika.ConnectionParameters(
    host=host,
    port=port,
    virtual_host=virtual_host,
    credentials=credentials,
    ssl_options=ssl_options
)

try:
    connection = pika.BlockingConnection(parameters)
    print("AMQP connection established successfully.")
    connection.close()
except pika.exceptions.AMQPError as e:
    print(f"AMQP connection failed: {e}")