# -*- coding: utf-8 -*-

# Copyright (2018) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json

from flask_api import status

from oneview_redfish_toolkit.blueprints import zone_collection
from oneview_redfish_toolkit.tests.base_flask_test import BaseFlaskTest


class TestZoneCollection(BaseFlaskTest):
    """Tests for ZoneCollection blueprint"""

    @classmethod
    def setUpClass(self):
        super(TestZoneCollection, self).setUpClass()

        self.app.register_blueprint(zone_collection.zone_collection)

        with open(
            'oneview_redfish_toolkit/mockups/oneview/'
            'ServerProfileTemplates.json'
        ) as f:
            self.server_profile_template_list = json.load(f)

        with open(
            'oneview_redfish_toolkit/mockups/redfish/ZoneCollection.json'
        ) as f:
            self.zone_collection_mockup = json.load(f)

        with open(
            'oneview_redfish_toolkit/mockups/oneview/'
            'LogicalEnclByIndexAssociationWithEnclGroup.json'
        ) as f:
            self.logical_encl_assoc = json.load(f)

        with open(
            'oneview_redfish_toolkit/mockups/oneview/LogicalEnclosure.json'
        ) as f:
            self.logical_encl = json.load(f)

        with open(
                'oneview_redfish_toolkit/mockups/oneview'
                '/Enclosures.json'
        ) as f:
            self.enclosures = json.load(f)

        with open(
                'oneview_redfish_toolkit/mockups/oneview'
                '/DriveEnclosureList.json'
        ) as f:
            self.drive_enclosure_list = json.load(f)

    def test_get_zone_collection_when_get_templates_raises_error(self):
        """Tests ZoneCollection when server profile templates raises error"""

        self.oneview_client.server_profile_templates.get_all.side_effect = \
            Exception()

        with open(
            'oneview_redfish_toolkit/mockups/errors/Error500.json'
        ) as f:
            error_500 = json.load(f)

        response = self.client.get(
            "/redfish/v1/CompositionService/ResourceZones/")

        result = json.loads(response.data.decode("utf-8"))

        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            response.status_code)
        self.assertEqual("application/json", response.mimetype)
        self.assertEqual(error_500, result)

    def test_get_zone_collection(self):
        """Tests ZoneCollection"""

        ov_api = self.oneview_client

        ov_api.connection.get.return_value = self.logical_encl_assoc
        ov_api.logical_enclosures.get.return_value = self.logical_encl

        ov_api.server_profile_templates.get_all.return_value = \
            self.server_profile_template_list
        ov_api.drive_enclosures.get_all.return_value = self.drive_enclosure_list
        ov_api.enclosures.get_all.return_value = self.enclosures

        response = self.client.get(
            "/redfish/v1/CompositionService/ResourceZones/")

        result = json.loads(response.data.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("application/json", response.mimetype)
        import pdb; pdb.set_trace()
        self.assertEqualMockup(self.zone_collection_mockup, result)

        spt_with_storage_ctrler = self.server_profile_template_list[0]
        ov_api.connection.get.assert_called_with(
            "/rest/index/associations/resources"
            "?parenturi=" + spt_with_storage_ctrler["enclosureGroupUri"]
            + "&category=logical-enclosures")
        ov_api.connection.get.assert_called_with(
            "/rest/index/associations/resources"
            "?parenturi=" + spt_with_storage_ctrler["enclosureGroupUri"]
            + "&category=logical-enclosures")
        ov_api.logical_enclosures.get.assert_called_with(self.logical_encl["uri"])
        ov_api.drive_enclosures.get_all.assert_called_with(
            filter="locationUri='/rest/enclosures/0000000000A66101'")
        ov_api.enclosures.get_all.assert_called_with()

    def test_get_zone_collection_empty(self):
        """Tests ZoneCollection with an empty list"""

        self.oneview_client.server_profile_templates.get_all.return_value = \
            []

        with open(
            'oneview_redfish_toolkit/mockups/redfish/ZoneCollectionEmpty.json'
        ) as f:
            zone_collection_empty_mockup = json.load(f)

        response = self.client.get(
            "/redfish/v1/CompositionService/ResourceZones/")

        result = json.loads(response.data.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("application/json", response.mimetype)
        self.assertEqualMockup(zone_collection_empty_mockup, result)

    def test_get_zone_collection_enclosure_without_drives(self):
        ov_api = self.oneview_client
        import pdb; pdb.set_trace()
        ov_api.connection.get.return_value = self.logical_encl_assoc
        ov_api.logical_enclosures.get.return_value = self.logical_encl

        ov_api.server_profile_templates.get_all.return_value = \
            self.server_profile_template_list
        ov_api.drive_enclosures.get_all.return_value = self.drive_enclosure_list
        ov_api.enclosures.get_all.return_value = self.enclosures

        response = self.client.get(
            "/redfish/v1/CompositionService/ResourceZones/")

        result = json.loads(response.data.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("application/json", response.mimetype)
        self.assertEqualMockup(self.zone_collection_mockup, result)

        spt_with_storage_ctrler = self.server_profile_template_list[0]
        ov_api.connection.get.assert_called_with(
            "/rest/index/associations/resources"
            "?parenturi=" + spt_with_storage_ctrler["enclosureGroupUri"]
            + "&category=logical-enclosures")
        ov_api.connection.get.assert_called_with(
            "/rest/index/associations/resources"
            "?parenturi=" + spt_with_storage_ctrler["enclosureGroupUri"]
            + "&category=logical-enclosures")
        ov_api.logical_enclosures.get.assert_called_with(self.logical_encl["uri"])
