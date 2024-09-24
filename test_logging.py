from logger import setup_logging
import logging

# Setup loggningen
setup_logging("test_log.log")

# Send a testlogg message
logging.info("This is a test log message.")
print("Logging test completed.")
