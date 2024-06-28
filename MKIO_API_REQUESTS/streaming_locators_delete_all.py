import json
import requests
import sys
import os
from aa_environment_params import setEnvironmentParams, MKIO_API_URL_PREFIX

def deleteAllStreamingLocators(params):
    """
    Deletes all streaming locators via MKIO API request from a given migration file.

    Parameters:
        `params` (namedtuple): available fields -- environment, fileName, contentKeyRestriction, subscriptionName
            -environment (str): the name of the environment (de, qa, stage)
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
        locatorName = locator["name"]
        assetName = locatorName.replace("locator", "output")

        # construct request
        url = f"{MKIO_API_URL_PREFIX}/{params.subscriptionName}/streamingLocators/{locatorName}"

        headers = {
            "accept": "application/json",
            "x-mkio-token": os.environ["MKIO_TOKEN"]
        }

        try:
            response = requests.delete(url, headers=headers)

            if response.status_code != 200 and response.status_code != 204:
                print(f"ERROR WITH DELETE REQUEST: Status code: {response.status_code} --- {assetName}")
                continue

            print(f"Successfully deleted streaming locator: {locatorName}")
        except Exception as e:
            print(f"ERROR DELETING STREAMING LOCATOR: {locatorName} - {str(e)}")

    file.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python delete_all_streaming_locators.py <environmentName: dev | qa | stage>")
        sys.exit(1)
    elif sys.argv[1] not in ["dev", "qa", "stage"]:
        print("Usage: python delete_all_streaming_locators.py <environmentName: dev | qa | stage>")
        sys.exit(1)

    environmentName = sys.argv[1]
    params = setEnvironmentParams(environmentName)
    deleteAllStreamingLocators(params)

if __name__ == "__main__":
    main()