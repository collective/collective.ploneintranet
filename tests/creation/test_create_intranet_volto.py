from AccessControl.users import nobody
from plone import api
from plone.distribution.api import site as site_api
from zope.component.hooks import setSite

import json
import pytest


DISTRIBUTION_NAME = "intranet-volto"
OAUTH_KEY_PREFIX = "pas.plugins.authomatic.interfaces.IPasPluginsAuthomaticSettings"


class TestPloneAuth:
    @pytest.fixture(autouse=True)
    def site_plone_auth(self, app):
        answers_plone_auth = {
            "site_id": "Intranet",
            "title": "Intranet with Plone Authentication",
            "description": "An intranet with Plone Authentication",
            "default_language": "en",
            "portal_timezone": "America/Sao_Paulo",
            "setup_content": True,
            "enable_discussion": True,
            "authentication": "Plone",
        }
        with api.env.adopt_roles(["Manager"]):
            site = site_api.create(app, DISTRIBUTION_NAME, answers_plone_auth)
            setSite(site)
        self.site = site

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ["id", "Intranet"],
            ["title", "Intranet with Plone Authentication"],
            ["description", "An intranet with Plone Authentication"],
        ],
    )
    def test_site_attributes(self, attr, expected):
        site = self.site
        assert getattr(site, attr) == expected

    @pytest.mark.parametrize(
        "object_id,portal_type",
        [
            ["images", "Document"],
            ["news", "Document"],
        ],
    )
    def test_site_content(self, object_id, portal_type):
        site = self.site
        object_ids = site.objectIds()
        assert object_id in object_ids
        assert site[object_id].portal_type == portal_type

    def test_site_permission(self):
        site = self.site
        review_state = api.content.get_state(site)
        assert review_state == "internal"

    @pytest.mark.parametrize(
        "permission,expected",
        [
            ["Access contents information", False],
            ["Modify portal contents", False],
            ["View", False],
        ],
    )
    def test_anonymous_permissions(self, permission, expected):
        site = self.site
        with api.env.adopt_user(user=nobody):
            user = api.user.get_current()
            assert api.user.has_permission(permission, user=user, obj=site) is expected

    def test_comments_enabled(self):
        value = api.portal.get_registry_record(
            "plone.app.discussion.interfaces.IDiscussionSettings.globally_enabled"
        )
        assert value is True


class TestPloneGitHub:
    @pytest.fixture(autouse=True)
    def site_plone_auth(self, app):
        answers_plone_auth = {
            "site_id": "Intranet",
            "title": "Intranet with GitHub Authentication",
            "description": "An intranet with GitHub Authentication",
            "default_language": "en",
            "portal_timezone": "America/Sao_Paulo",
            "setup_content": True,
            "authentication": "GitHub",
            "consumer_key": "foo",
            "consumer_secret": "bar",
        }
        with api.env.adopt_roles(["Manager"]):
            site = site_api.create(app, DISTRIBUTION_NAME, answers_plone_auth)
            setSite(site)
        self.site = site

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ["id", "Intranet"],
            ["title", "Intranet with GitHub Authentication"],
            ["description", "An intranet with GitHub Authentication"],
        ],
    )
    def test_site_attributes(self, attr, expected):
        site = self.site
        assert getattr(site, attr) == expected

    def test_site_authomatic_settings(self):
        json_config = json.loads(
            api.portal.get_registry_record(f"{OAUTH_KEY_PREFIX}.json_config")
        )
        assert "github" in json_config
        assert json_config["github"]["consumer_key"] == "foo"
        assert json_config["github"]["consumer_secret"] == "bar"


class TestPloneGoogle:
    @pytest.fixture(autouse=True)
    def site_plone_auth(self, app):
        answers_plone_auth = {
            "site_id": "Intranet",
            "title": "Intranet with Google Authentication",
            "description": "An intranet with Google Authentication",
            "default_language": "en",
            "portal_timezone": "America/Sao_Paulo",
            "setup_content": True,
            "enable_discussion": False,
            "authentication": "Google",
            "consumer_key": "foo",
            "consumer_secret": "bar",
            "auth_scope": "['profile', 'email']",
        }
        with api.env.adopt_roles(["Manager"]):
            site = site_api.create(app, DISTRIBUTION_NAME, answers_plone_auth)
            setSite(site)
        self.site = site

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ["id", "Intranet"],
            ["title", "Intranet with Google Authentication"],
            ["description", "An intranet with Google Authentication"],
        ],
    )
    def test_site_attributes(self, attr, expected):
        site = self.site
        assert getattr(site, attr) == expected

    def test_site_authomatic_settings(self):
        json_config = json.loads(
            api.portal.get_registry_record(f"{OAUTH_KEY_PREFIX}.json_config")
        )
        assert "google" in json_config
        assert json_config["google"]["consumer_key"] == "foo"
        assert json_config["google"]["consumer_secret"] == "bar"
