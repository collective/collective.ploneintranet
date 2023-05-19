"""Handle Logins."""
from collective.ploneintranet import logger
from plone import api

import os


ADMIN_GROUP = "Site Administrators"

OAUTH_AUTOMEMBER = os.environ.get("OAUTH_AUTOMEMBER", None)
OAUTH_AUTOADMIN = os.environ.get("OAUTH_AUTOADMIN", None)


def first_login_handler(event):
    """Add user to correct Group."""
    user = event.object
    username = user.getUserName()
    with api.env.adopt_roles(["Manager"]):
        if OAUTH_AUTOADMIN:
            group = api.group.get(groupname=ADMIN_GROUP)
            admins = [m for m in api.user.get_users(group=group)]
            if len(admins) == 0:
                api.group.add_user(groupname=ADMIN_GROUP, username=username)
                logger.info(f"Added user {username} to {ADMIN_GROUP}")
        elif OAUTH_AUTOMEMBER:
            api.user.grant_roles(user=user, roles=["Member"])
            logger.info(f"Set user {username} as member")
