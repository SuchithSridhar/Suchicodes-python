from datetime import datetime
import flask as f
from ..config import Config
from ..models import Extern_Messages
from ..util import Util
from .. import db, logger
from .. import models
from ..controllers.resources.res_util import ResUtil


cli_blueprint = f.Blueprint("cli_commands", __name__)


@cli_blueprint.cli.command()
def server_checkin_task():
    """Task to check if server reporting correctly.

    To be called every THRESHOLD_MINS : flask cli_commands server-checkin-task
    using cronjobs.
    """

    THRESHOLD = Config.THRESHOLD_MINS * 60
    cur_date = datetime.now()
    servers = [Config.ASTRAX_SERVER_TAG, Config.BERNUM_SERVER_TAG]
    logger.info("Starting server_checkin_task")

    for server in servers:
        data = (
            Extern_Messages.query.filter(Extern_Messages.tags.like(f"%#{server}$%"))
            .filter(Extern_Messages.tags.like(f"%#{Config.SERVER_OFFLINE_TAG}$%"))
            .first()
        )

        if data is not None:
            logger.info("Server %s already marked offline", server)
            # Server already marked as offline
            continue

        data_list = (
            Extern_Messages.query.filter(Extern_Messages.tags.like(f"%#{server}$%"))
            .filter(Extern_Messages.tags.like(f"%#{Config.SERVER_CHECKIN_TAG}$%"))
            .order_by(Extern_Messages.timestamp.desc())
        )

        last_message = data_list.first()

        # Delete messages over the checkin limit
        to_delete = data_list[Config.CHECKIN_LIMIT :]
        for item in to_delete:
            db.session.delete(item)

        db.session.commit()

        # No logs yet - server hasn't reported once
        if last_message is None:
            logger.info("No logs recieved from server %s.", server)
            continue

        last_date = last_message.timestamp
        difference = cur_date - last_date

        total_seconds = difference.total_seconds()

        if total_seconds < THRESHOLD:
            logger.info("Server %s within threshold limit.", server)
            # everything is fine, just ignore
            continue

        # === The server is not reporting as necessary ===

        id = Util.create_uuid()
        offline_message = Extern_Messages(
            id=id,
            user=Config.INTERNAL_USER,
            message=f"{server} is offline",
            timestamp=cur_date,
            tags=Extern_Messages.create_tags([server, Config.SERVER_OFFLINE_TAG]),
        )

        db.session.add(offline_message)
        db.session.commit()

        logger.warn("Server %s not reporting, alert sent out.", server)
        Util.send_notification(
            f"Suchicodes: {server} status",
            f"Server seems to be offline. Last message at: {last_date}.",
            priority=9,
        )

    logger.info("server_checkin_task complete.")


@cli_blueprint.cli.command()
def replace_math_string_markdown():
    """Function to replace the $$$ and $$ with $$ and $ respectively.

    This is designed to only be called once. Ever.
    """

    def update_markdown(markdown: str) -> str:

        placeholder = "#dhjwnecvyq#"
        markdown = markdown.replace("$$$", placeholder)
        markdown = markdown.replace("$$", "$")
        markdown = markdown.replace(placeholder, "$$")
        return markdown

    blogs: list[models.Blog] = models.Blog.query.all()
    for blog in blogs:
        # If this substring is present then it needs to be updated
        if "$$$" in blog.markdown:
            blog.markdown = update_markdown(blog.markdown)
            logger.warn(f"Updated blog with ID: {blog.id[:6]}, and title: {blog.title}")
            blog.html = ResUtil.to_html(blog.markdown)

    db.session.commit()
