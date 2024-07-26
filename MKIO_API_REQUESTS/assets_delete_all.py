import requests
import json
import sys
import os
from aa_environment_params import setEnvironmentParams, MKIO_API_URL_PREFIX

def deleteAllAssets(selectedBaseUrl: str):
    """
    Deletes all assets via MKIO API request from a given migration file.

    Parameters:
        `selectedBaseUrl` (str): the selected base URL based on the environment name
    """

    # 1. List all assets
    headers = {
        "accept": "application/json",
        "x-mkio-token": os.environ["MKIO_TOKEN"]
    }

    response = requests.get(selectedBaseUrl, headers=headers)
    assets = json.loads(response.text)


    # 2. Delete all assets
    for i in range(len(assets['value'])):
        try:
            url = f"{selectedBaseUrl}/{assets['value'][i]['name']}"

            response = requests.delete(url, headers=headers)
            if response.status_code != 200 and response.status_code != 204:
                print(f"ERROR WITH DELETE REQUEST: Status code: {response.status_code} --- {assets['value'][i]['name']}")
                continue

            print(f"Successfully deleted asset: {assets['value'][i]['name']}")
        except:
            print(f"ERROR DELETING ASSET: {assets['value'][i]['name']}")
    

def main():
    if len(sys.argv) != 2:
        print("Usage: python assets_delete_all.py <environmentName: dev | qa | stage | prod>")
        sys.exit(1)
    elif sys.argv[1] not in ["dev", "qa", "stage", "prod"]:
        print("Usage: python assets_delete_all.py <environmentName: dev | qa | stage | prod>")
        sys.exit(1)

    environmentName = sys.argv[1]
    params = setEnvironmentParams(environmentName)
    selectedBaseUrl = f"{MKIO_API_URL_PREFIX}/{params.subscriptionName}/assets"
    deleteAllAssets(selectedBaseUrl)

if __name__ == "__main__":
    main()
