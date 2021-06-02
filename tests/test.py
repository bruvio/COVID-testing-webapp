import os
import sys
import unittest

import numpy as np
import requests

# sys.path.append("../")

topdir = os.path.join(os.path.dirname(__file__), "..")
# print(topdir)
sys.path.append(topdir)

path = os.getcwd()
# print("Current Directory", path)

# prints parent directory
# print(os.path.abspath(os.path.join(path, os.pardir)))
# print(os.path.dirname(__file__))
from src.server import server

try:
    print("deleting database")
    # import pdb
    # pdb.set_trace()
    os.remove(path + "/src/data.db")
    print("database deleted")
except:
    print("failed to delete database")
    pass


def authenticate():
    # first authenticate
    url = "http://127.0.0.1:8000/auth"

    payload = '{\n\t"username": "bruno",\n\t"password": "asdf"\n}\n'
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    # token = response.text.decode("utf8")
    token = response.json()["access_token"]
    return response.status_code, token


class ProjectTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        server.config["TESTING"] = True
        server.config["DEBUG"] = False
        self.app = server.test_client()

        self.assertEqual(server.debug, False)

    # executed after each test
    def tearDown(self):
        super(ProjectTests, self).tearDown()

    ########################
    #### helper methods ####
    ########################

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)

        assert response.status_code == 200
        assert response.data == b"Hello, bruvio!"

    def test_register(self):

        url = "http://127.0.0.1:8000/register"

        payload = '{\n\t"username": "bruno",\n\t"password": "asdf"\n}\n'
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.json()["message"])
        assert response.status_code == 400  # user already exists

    # # #
    # # # #
    # #
    def test_auth(self):
        status, dummy = authenticate()

        assert status == 200

    # # #
    # # # #

    # # #
    def test_post_resource_doesnot_exist(self):
        status, token = authenticate()

        url = "http://127.0.0.1:8000/cartridge/DN4110004145909" + str(
            np.random.randint(low=0, high=100, size=1)
        )

        payload = '{\n\t"cartridgeId": "DN4110004145909",\n\t"testStatus": "Error",\n\t"departmentName": "DPT001",\n\t"boxName": "nudge_2294DC",\n\t"pattern": "CVD540",\n\t"hospitalName": "HSP001",\n\t"operatorName": "opt1",\n\t"organisationId": "ORG1",\n\t"participantId": "V8Z85",\n\t"trustName": "TRUST1",\n\t"submissionDateTime": "2021-03-04 10:59:40.000 UTC",\n\t"testStartDateTime": "2021-03-04 11:01:55.000 UTC",\n\t"lastUpdatedDateTime": "2021-03-04 13:55:58.192 UTC"\n}'

        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT  " + str(token),
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # print('test_post_resource_doesnot_exist',(response.status_code))
        assert response.status_code == 500

    def test_post_resource_already_exists(self):
        status, token = authenticate()
        url = "http://127.0.0.1:8000/cartridge/DN4110004145909"

        payload = '{\n\t"cartridgeId": "DN4110004145909",\n\t"testStatus": "Error",\n\t"departmentName": "DPT001",\n\t"boxName": "nudge_2294DC",\n\t"pattern": "CVD540",\n\t"hospitalName": "HSP001",\n\t"operatorName": "opt1",\n\t"organisationId": "ORG1",\n\t"participantId": "V8Z85",\n\t"trustName": "TRUST1",\n\t"submissionDateTime": "2021-03-04 10:59:40.000 UTC",\n\t"testStartDateTime": "2021-03-04 11:01:55.000 UTC",\n\t"lastUpdatedDateTime": "2021-03-04 13:55:58.192 UTC"\n}'

        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT  " + str(token),
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # print('test_post_resource_already_exists',(response.status_code))
        assert response.status_code == 201

    def test_delete(self):
        status, token = authenticate()

        url = "http://127.0.0.1:8000/cartridge/DN4110004145909"

        payload = {}
        headers = {
            "Authorization": "JWT " + str(token),
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)
        assert response.json()["message"] == "cartridge not found."

    def test_cartridges(self):
        status, token = authenticate()

        url = "http://127.0.0.1:8000/cartridges"

        payload = {}
        headers = {
            "Authorization": "JWT " + str(token),
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text.encode("utf8"))
        # print(dir(response))
        # print((response.status_code))
        assert response.status_code == 202


if __name__ == "__main__":
    import xmlrunner

    runner = xmlrunner.XMLTestRunner(output="tests/test-reports")
    unittest.main(testRunner=runner)
    ###########################################
    unittest.main()
