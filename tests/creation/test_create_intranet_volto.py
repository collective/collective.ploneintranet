from AccessControl.users import nobody
from plone import api
from plone.distribution.api import site as site_api
from zope.component.hooks import setSite

import pytest


DISTRIBUTION_NAME = "intranet-volto"


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
