"""
A subsriber object for nodes
"""

import socket
import json
import logging
import threading


class Subscriber:
    """
    Subscriber class for myROS.

    Allows nodes to subscribe to messages from a specified topic.
    """
