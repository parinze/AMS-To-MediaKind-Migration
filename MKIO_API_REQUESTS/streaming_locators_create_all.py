import json
import requests
import sys
import os
from aa_environment_params import setEnvironmentParams, MKIO_API_URL_PREFIX

def createAllStreamingLocators(params):
    """
    Creates all streaming locators via MKIO API request from a given migration file.

    Parameters:
        `params` (namedtuple): available fields -- environment, fileName, contentKeyRestriction, subscriptionName
            -environment (str): the name of the environment (de, qa, stage, prod)
            -fileName (str): the name of the migration file
            -contentKeyRestriction (dict): the content key restriction information
                    -Issuer (str): the issuer
                    -PrimaryVerificationKey (str): the primary verification key
            -subscriptionName (str): the name of the subscription
    """

    file = open(f"C:\\ams-migration-tool\\{params.fileName}", "r")

    data = json.load(file)

    streamingLocators = data["StreamingLocators"]

    for locator in streamingLocators:
        properties = locator["properties"]
        contentKey = properties["contentKeys"][0]

        locatorName = locator["name"]

        assetName = properties["assetName"]
        locatorDefaultContentKeyPolicyName = properties["defaultContentKeyPolicyName"]
        locatorEndTime = properties["endTime"]
        locatorStreamingLocatorId = properties["streamingLocatorId"]
        locatorStreamingPolicyName = properties["streamingPolicyName"]
        contentKeyId = contentKey["id"]
        contentKeyLabel = "cencDefaultKey" # migration document has the incorrect value ("cencKeyDefault")
        contentKeyPolicy = contentKey["policyName"]
        contentKeyType = contentKey["type"]
        contentKeyValue = contentKey["value"]


        # construct request
        url = f"{MKIO_API_URL_PREFIX}/{params.subscriptionName}/streamingLocators/{locatorName}"

        # payload = {
        #     "properties": {
        #         "assetName": assetName.strip(),
        #         "contentKeys": [
        #             {
        #                 "id": contentKeyId.strip(),
        #                 "labelReferenceInStreamingPolicy": contentKeyLabel.strip(),
        #                 "policyName": contentKeyPolicy.strip(),
        #                 "type": contentKeyType.strip(),
        #                 "value": contentKeyValue.strip()
        #             }
        #         ],
        #         "defaultContentKeyPolicyName": locatorDefaultContentKeyPolicyName.strip(),
        #         "endTime": locatorEndTime.strip(),
        #         "streamingLocatorId": locatorStreamingLocatorId.strip(),
        #         "streamingPolicyName": locatorStreamingPolicyName.strip()
        #     }
        # }

        payload = { 
            "properties": {
                "assetName": assetName,
                "defaultContentKeyPolicyName": "DRMContentKeyPolicy",
                "streamingPolicyName": "Predefined_MultiDrmCencStreaming"
            } 
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-mkio-token": os.environ["MKIO_TOKEN"]
        }

        try:
            response = requests.put(url, json=payload, headers=headers)
            parsedResponse = response.json()

            if ("error" in parsedResponse):
                print(f"ERROR PARSING RESPONSE: {assetName} --- {parsedResponse}")
                continue

            print(f"Successfully created streaming locator: {locatorName}")
        except:
            print(f"ERROR DELETING STREAMING LOCATOR: {locatorName}")


    file.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python create_all_streaming_locators.py <environmentName: dev | qa | stage | prod>")
        sys.exit(1)
    elif sys.argv[1] not in ["dev", "qa", "stage", "prod"]:
        print("Usage: python create_all_streaming_locators.py <environmentName: dev | qa | stage | prod>")
        sys.exit(1)

    environmentName = sys.argv[1]
    params = setEnvironmentParams(environmentName)
    createAllStreamingLocators(params)

if __name__ == "__main__":
    main()