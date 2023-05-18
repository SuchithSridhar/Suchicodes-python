from datetime import datetime
import flask as f
from ..config import Config
from ..models import Extern_Messages
from ..util import Util
from .. import db, logger

cli_blueprint = f.Blueprint('cli_commands', __name__)

@cli_blueprint.cli.command()
def server_checkin_task():
    """
    Task to check if server reporting correctly.
    To be called every 20 mins: flask cli_commands server-checkin-task
    using cronjobs.
    """

    # 20 mins in seconds
    THRESHOLD = 20 * 60
    cur_date = datetime.now()
    servers = [ Config.ASTRAX_SERVER_TAG, Config.BERNUM_SERVER_TAG]
    logger.info('Starting server_checkin_task')


    for server in servers:
        data = Extern_Messages.query \
                .filter(Extern_Messages.tags.like(f'%#{server}$%')) \
                .filter(Extern_Messages.tags.like(f'%#{Config.SERVER_OFFLINE_TAG}$%')) \
                .first()

        if data != None:
            logger.info('Server %s already marked offline', server)
            # Server already marked as offline
            continue

        last_message = Extern_Messages.query \
                   .filter(Extern_Messages.tags.like(f'%#{server}$%')) \
                   .filter(Extern_Messages.tags.like(f'%#{Config.SERVER_CHECKIN_TAG}$%')) \
                   .order_by(Extern_Messages.timestamp.desc()).first()

        # No logs yet - server hasn't reported once
        if last_message is None:
            logger.info('No logs recieved from server %s.', server)
            continue

        last_date = last_message.timestamp
        difference = cur_date - last_date

        total_seconds = difference.total_seconds()

        if total_seconds < THRESHOLD:
            logger.info('Server %s within threshold limit.', server)
            # everything is fine, just ignore
            continue

        # === The server is not reporting as necessary ===

        id = Util.create_uuid()
        offline_message = Extern_Messages(
            id = id,
            user = Config.INTERNAL_USER,
            message = f"{server} is offline",
            timestamp = cur_date,
            tags = Extern_Messages.create_tags([server, Config.SERVER_OFFLINE_TAG])
        )

        db.session.add(offline_message)
        db.session.commit()

        logger.warn('Server %s not reporting, alert sent out.', server)
        Util.send_notification_to_IFFF(f"{server} not reporting.")

    logger.info('server_checkin_task complete.')
