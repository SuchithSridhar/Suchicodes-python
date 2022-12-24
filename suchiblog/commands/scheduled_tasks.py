import os
from datetime import datetime
import flask as f
from ..config import Config
from ..util import Util

cli_blueprint = f.Blueprint('cli_commands', __name__)


@cli_blueprint.cli.command()
def server_checkin_task():
    """Task to check if server reporting correctly"""

    # 20 mins in seconds
    THRESHOLD = 20 * 60
    cur_date = datetime.now()

    # if this file exists then a notification was already sent.
    if (os.path.isfile(Config.SUCHI_SERVER_VAIDATION)):
        return

    if (os.path.isfile(Config.SUCHI_SERVER_CHECKIN_FILE)):

        with open(Config.SUCHI_SERVER_CHECKIN_FILE) as checkin_file:
            data = checkin_file.read()

        # get the date on the last line
        try:
            data = data.strip().split("\n")[-1].split(",")[0]

        except Exception:
            pass

        else:
            last_date = datetime.strptime(
                data,
                Config.DATETIME_COMPLETE_FORMAT
            )
            difference = cur_date - last_date
            total_seconds = difference.total_seconds()

            if total_seconds < THRESHOLD:
                # everything is fine, just ignore
                return

    # The server is not reporting as necessary.
    with open(Config.SUCHI_SERVER_VAIDATION, "w") as validation_file:
        validation_file.write(
            cur_date.strftime(Config.DATETIME_COMPLETE_FORMAT)
        )

    Util.send_notification_to_IFFF("Server not reporting")
