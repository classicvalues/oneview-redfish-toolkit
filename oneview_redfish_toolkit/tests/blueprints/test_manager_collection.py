# -*- coding: utf-8 -*-

# Copyright (2017-2018) Hewlett Packard Enterprise Development LP
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

# Python libs
import json

# 3rd party libs
from flask_api import status

# Module libs
from oneview_redfish_toolkit.blueprints import manager_collection
from oneview_redfish_toolkit.tests.base_flask_test import BaseFlaskTest


class TestManagerCollection(BaseFlaskTest):
    """Tests for ManagerCollection blueprint

        Tests:
            - server hardware empty
            - enclosures empty
            - oneview unexpected exception
            - know manager collection
    """

    @classmethod
    def setUpClass(self):
        super(TestManagerCollection, self).setUpClass()

        self.app.register_blueprint(
            manager_collection.manager_collection)

    def test_get_manager_collection_unexpected_error(
            self):
        """Tests ManagerCollection with an error"""

        self.oneview_client.server_hardware.get_all.side_effect = Exception()

        with open(
                'oneview_redfish_toolkit/mockups/errors/'
                'Error500.json'
        ) as f:
            error_500 = json.load(f)

        response = self.client.get("/redfish/v1/Managers/")

        result = json.loads(response.data.decode("utf-8"))

        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            response.status_code)
        self.assertEqual("application/json", response.mimetype)
        self.assertEqual(error_500, result)

    def test_get_manager_collection_empty(self):
        """Tests ManagerCollection with enclosures response empty"""

        self.oneview_client.server_hardware.get_all.return_value = []
        self.oneview_client.enclosures.get_all.return_value = []

        with open(
                'oneview_redfish_toolkit/mockups/redfish/'
                'ManagerCollectionEmpty.json'
        ) as f:
            manager_collection_empty = json.load(f)

        response = self.client.get("/redfish/v1/Managers/")
        result = json.loads(response.data.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("application/json", response.mimetype)
        self.assertEqual(manager_collection_empty, result)

    def test_get_manager_collection(self):
        """Tests a valid ManagerCollection"""

        # Loading server_hardware mockup value
        with open(
            'oneview_redfish_toolkit/mockups/oneview/'
            'ServerHardwareList.json'
        ) as f:
            server_hardware_list = json.load(f)

        # Loading enclosures mockup value
        with open(
            'oneview_redfish_toolkit/mockups/oneview/'
            'Enclosures.json'
        ) as f:
            enclosures = json.load(f)

        with open(
                'oneview_redfish_toolkit/mockups/redfish/'
                'ManagerCollection.json'
        ) as f:
            manager_collection_mockup = json.load(f)

        # Create mock response
        self.oneview_client.server_hardware.get_all.return_value = \
            server_hardware_list
        self.oneview_client.enclosures.get_all.return_value = enclosures

        # Get ManagerCollection
        response = self.client.get("/redfish/v1/Managers/")

        # Gets json from response
        result = json.loads(response.data.decode("utf-8"))

        # Tests response
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("application/json", response.mimetype)
        self.assertEqualMockup(manager_collection_mockup, result)
