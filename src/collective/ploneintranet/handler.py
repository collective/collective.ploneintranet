from plone import api
from plone.distribution.core import Distribution
from Products.CMFPlone.Portal import PloneSite

import json


KEY = "pas.plugins.authomatic.interfaces.IPasPluginsAuthomaticSettings.json_config"


GOOGLE = """{
    "google": {
        "id": 1,
        "display": {
            "title": "Google",
            "cssclasses": {
                "button": "plone-btn plone-btn-default",
                "icon": "glypicon glyphicon-google"
            },
            "as_form": false
        },
        "propertymap": {
            "email": "email",
            "link": "home_page",
            "name": "fullname",
            "picture": "portrait"
        },
        "class_": "authomatic.providers.oauth2.Google",
        "consumer_key": "##consumer_key##",
        "consumer_secret": "##consumer_secret##",
        "scope": ##auth_scope##,
        "access_headers": {
            "User-Agent": "Plone (pas.plugins.authomatic)"
        }
    }
}
"""

GITHUB = """{
    "github": {
        "id": 1,
        "display": {
            "title": "Github",
            "cssclasses": {
                "button": "plone-btn plone-btn-default",
                "icon": "glypicon glyphicon-github"
            },
            "as_form": false
        },
        "propertymap": {
            "email": "email",
            "link": "home_page",
            "location": "location",
            "name": "fullname",
            "avatar_url": "portrait",
            "username": "github_username"
        },
        "class_": "authomatic.providers.oauth2.GitHub",
        "consumer_key": "##consumer_key##",
        "consumer_secret": "##consumer_secret##",
        "access_headers": {
            "User-Agent": "Plone (pas.plugins.authomatic)"
        }
    }
}"""


def post_handler(
    distribution: Distribution, site: PloneSite, answers: dict
) -> PloneSite:
    """Adjust installation."""
    # Update security
    wf_tool = api.portal.get_tool("portal_workflow")
    wf_tool.updateRoleMappings()
    # enable_discussion
    enable_discussion = answers.get("enable_discussion", False)
    api.portal.set_registry_record(
        "plone.app.discussion.interfaces.IDiscussionSettings.globally_enabled",
        enable_discussion,
    )

    # Process answers
    profiles = distribution.profiles
    authentication = answers.get("authentication", "Plone")
    if authentication == "Plone":
        return site
    setup_tool = site["portal_setup"]
    # Install profile
    profiles = [
        "collective.ploneintranet:oauth",
    ]
    for profile_id in profiles:
        setup_tool.runAllImportStepsFromProfile(f"profile-{profile_id}")

    config = api.portal.get_registry_record(KEY)

    keys = [
        "consumer_key",
        "consumer_secret",
    ]
    if authentication.startswith("Google"):
        base = GOOGLE
        keys = ["consumer_key", "consumer_secret", "auth_scope"]
        answers["auth_scope"] = answers["auth_scope"].replace("'", '"')
    elif authentication.startswith("GitHub"):
        base = GITHUB

    for key in keys:
        base = base.replace(f"##{key}##", answers.get(key))

    # Poor's man validation
    data = json.loads(base)
    config = json.dumps(data, indent=2)
    api.portal.set_registry_record(KEY, config)
    return site
