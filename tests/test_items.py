import allure
import pytest

from consts import consts
from tools.helper import random_uuid
from tools.logger import get_logger

logger = get_logger(name="main_logger")


class Test1:

    @pytest.mark.parametrize("test_url, test_md5, common_profile_id, profile_id",
                             [
                                 (consts.url, consts.md, consts.commonid, consts.profileid),
                                 (...),
                             ],
                             ids=[
                                 "first",
                                 "second"
                             ]
                             )
    def test_ingest_e2e(self, meta1_api_client, mata2_api_client, mata3_api_client,
                              test_url, test_md5, common_profile_id, vs_profile_id):
        external_id, do_external_id = random_uuid(), random_uuid()
        id, content_id = ingest(
            external_id=external_id,
            do_external_id=do_external_id,
            variables=VARIABLES,
            api_client=meta1_api_client,
            test_url=test_url,
            test_md5=test_md5
        )
        logger.info(f"Got id from ... : [{id}]")

        with allure.step(f"Verify status for  {id}"):
            status = wait_status_success(id=id, mata2_api_client=mata2_api_client)
            assert status == consts.TaskStates.SUCCESS.value
        with allure.step("Verify ... in db, expect success status"):
            task = verify_tasks(id=id, profile_id=consts.profileid)
            assert task in consts.TaskStates.list(), "Test failed, actual status is undefined"
        with allure.step("Verify ..., expect http OK status"):
            meta3_request(id, meta3_api_client)

        for profile_id in vs_profile_id:
            logger.info(f"---------Start verify tasks for profile: {profile_id}---------")
            with allure.step(f"Verify ... status for  {id} and  profile {profile_id}"):
                actual_result = send_request(id=id, profile_id=profile_id)
                task_state, location = actual_result["task_state"],actual_result["location"]
                assert task_state == consts.TaskStates.SUCCESS.value, f"Test failed, actual state is: {task_state}"
                assert location is not None, f"Test failed, location is None"

class Test2:

    @pytest.mark.parametrize("test_url, md5, language",
                             [
                                 (url_eng, md5, "eng"),
                             ],
                             ids=
                             [
                                 "english"
                             ])
    def test_add_one_language(self, meta1_api_client, mata2_api_client, mata3_api_client, test_url, md5, language):
        expected_sbtl_list = []
        external_id, id = prepare_item(meta1_api_client, mata2_api_client, mata3_api_client)
        with allure.step(f"Add {language} for item {id}"):
            lan_id, id, description, parent_id = ingest_language(
                external_id=external_id,
                meta1_api_client=meta1_api_client,
                test_url=test_url,
                md5=md5,
                language=language
            )
        logger.info(f"Got lan_id from ... : [{lan_id}]")
        logger.info(f"Got description from .. : [{description}]")
        assert parent_id == id, f"Test failed, ids do not match"
        expected_sbtl_list.append(description)

        with allure.step(f"Verify ingest status for language {lan_id}"):
            ingest_status = wait_status(lan_id=lan_id,
                                                 mata2_api_client=mata2_api_client,
                                                 expected_data=consts.TaskStates.SUCCESS.value)
            assert ingest_status == consts.TaskStates.SUCCESS.value

        with allure.step("Verify meta3 got right list of languages"):
            languages = wait_lan_in_meta2(id, mata3_api_client)
            assert len(languages) == len(expected_sbtl_list), "Test failed, list is not complete"
            for sbtl in languages:
                logger.info(f" language tag from meta3: {sbtl['tag']}")
                assert sbtl["tag"] in expected_sbtl_list, "Test failed, wrong tag"
                assert sbtl["url"] is not None, "Test failed, url is empty"
