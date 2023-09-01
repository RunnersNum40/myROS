"""
A publisher object for nodes
"""

import socket
import json
import logging
import threading


class Publisher:
    """
    Publisher class for myROS.

    Allows nodes to publish messages to a specified topic.
    """

    buffer_size: int = 1024

    def __init__(self, node_name: str, topic: str, core_socket_path: str) -> None:
        """
        Initialize the publisher with a node name and topic.

        :param node_name: Name of the node.
        :param topic: Topic to publish to.
        :param core_socket_path: Path to the core's Unix Domain Socket.
        """
        self.node_name = node_name
        self.topic = topic
        self.core_socket_path = core_socket_path
        self.uds_path = (
            None  # Will store the UDS path provided by the Core for this publisher
        )

        self.register_with_core()
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.start()

    def register_with_core(self) -> None:
        """Register the publisher with the myROS Core."""
        message = {
            "action": "publisher_register",
            "data": {"name": self.node_name, "topic": self.topic},
        }

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as core_socket:
            try:
                core_socket.connect(self.core_socket_path)
                core_socket.sendall(json.dumps(message).encode("utf-8"))
                response = json.loads(
                    core_socket.recv(self.buffer_size).decode("utf-8")
                )
                if response.get("status") == "success":
                    self.uds_path = response.get("uds_path")
                    logging.info(
                        "Publisher registered with UDS path: %s", self.uds_path
                    )
                else:
                    logging.error("Failed to register publisher with Core.")
            except socket.error as error:
                logging.error("Socket error: %s", str(error))

    def publish(self, message_data: dict) -> None:
        """Publish a message to the topic."""
        # The actual logic for publishing would typically involve using the UDS path
        # and communicating the message to subscribers through the Core.
        # For simplicity, I'll just log the publishing action here.
        logging.info("Publishing message to topic %s: %s", self.topic, message_data)
        # In a more complete system, you'd send this message data to the Core or directly to subscribers.

    def run(self):
        """Establish connections with new subscribers"""
        # Create a socket and bind it to the uds path provide by the core
        # Handle new subscriber registrations
        pass


if __name__ == "__main__":
    # Sample usage for testing
    publisher = Publisher(
        node_name="Temperature",
        topic="Temperature",
        core_socket_path="/run/myROS_core.sock",
    )
    publisher.publish({"temp": 23.5})
