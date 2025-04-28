import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# Create the logger
debuglog = logging.getLogger("my_logger")

debuglog.log(logging.CRITICAL, "OMG THE WORLD IS ENDING!!!!")

debuglog.critical("there is no more disk space")
debuglog.error("file not found creating new file")
debuglog.warning("disk space is low")
debuglog.info("user logged in with correct password")


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s: %(name)s',force=True)

logging.getLogger("my_app")
logging.getLogger("my_app.utils")
logging.getLogger("my_app.utils.db")

formatter = logging.Formatter(
    fmt=(
        "%(asctime)s | %(levelname)s | "
        "%(message)s"
    )
)

# couldn't figure it out completely but I put as much as I could together from the lecture