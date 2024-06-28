import requests
import os

subscription_dev = "dolphmediasvc301_dev"
subscription_qa = "dolphmediasvc101_qa"
subscription_stage = "dolphmediasvc201_stage"

dev_params = [subscription_dev, "generated_migration_files/DEV_streaming_locators.txt"]
qa_params = [subscription_qa, "generated_migration_files/QA_streaming_locators.txt"]
stage_params = [subscription_stage, "generated_migration_files/STAGE_streaming_locators.txt"]



for selectedParams in (dev_params, qa_params, stage_params):

    subscriptionName = selectedParams[0]
    locatorsFile = selectedParams[1]

    with open(locatorsFile, "r") as loc_file:
        for l in loc_file:
            locator = l.strip()
            url = f"https://api.mk.io/api/ams/{subscriptionName}/streamingLocators/{locator}/listPaths"

            headers = {
                "accept": "application/json",
                "x-mkio-token": os.environ["MKIO_TOKEN"]
            }

            response = requests.post(url, headers=headers)
            data = response.json()

            with open(f"generated_migration_files/x_STREAMING_URLS_{selectedParams[0]}.txt", "a") as output_file:
                output_file.write(f"{locator} - {data['streamingPaths'][0]['paths'][0]}\n")

            print(f"{locator} - {data['streamingPaths'][0]['paths'][0]}")