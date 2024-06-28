import requests
import sys
import os
from aa_environment_params import setEnvironmentParams, MKIO_API_URL_PREFIX

def overwriteContentKeyPolicy(params):
    """
   Overwrites content key policy via MKIO API request.

    Parameters:
        `params` (namedtuple): available fields -- environment, fileName, contentKeyRestriction, subscriptionName
            -environment (str): the name of the environment (de, qa, stage)
            -fileName (str): the name of the migration file
            -contentKeyRestriction (dict): the content key restriction information
                    -Issuer (str): the issuer
                    -PrimaryVerificationKey (str): the primary verification key
            -subscriptionName (str): the name of the subscription
    """

    url = f"{MKIO_API_URL_PREFIX}/{params.subscriptionName}/contentKeyPolicies/DRMContentKeyPolicy"

    audience = "AqDrmAudience"
    customClaimTypeName = "urn:microsoft:azure:mediaservices:contentkeyidentifier"

    payload = { "properties": { "options": [
            {
                "configuration": {
                    "@odata.type": "#Microsoft.Media.ContentKeyPolicyPlayReadyConfiguration",
                    "licenses": [
                        {
                            "allowTestDevices": True,
                            "contentKeyLocation": { "@odata.type": "#Microsoft.Media.ContentKeyPolicyPlayReadyContentEncryptionKeyFromHeader" },
                            "contentType": "UltraVioletStreaming",
                            "licenseType": "Persistent",
                            "playRight": {
                                "allowPassingVideoContentToUnknownOutput": "Allowed",
                                "digitalVideoOnlyContentRestriction": False,
                                "explicitAnalogTelevisionOutputRestriction": {
                                    "bestEffort": True,
                                    "configurationData": 2
                                },
                                "imageConstraintForAnalogComponentVideoRestriction": True,
                                "imageConstraintForAnalogComputerMonitorRestriction": False
                            },
                            "beginDate": "2015-12-31T18:00:00Z",
                            "securityLevel": "SL150"
                        }
                    ]
                },
                "restriction": {
                    "primaryVerificationKey": {
                        "@odata.type": "#Microsoft.Media.ContentKeyPolicySymmetricTokenKey",
                        "keyValue": params.contentKeyRestriction["PrimaryVerificationKey"]
                    },
                    "restrictionTokenType": "Jwt",
                    "@odata.type": "#Microsoft.Media.ContentKeyPolicyTokenRestriction",
                    "issuer": params.contentKeyRestriction["Issuer"],
                    "audience": audience,
                    "requiredClaims": [{ "claimType": customClaimTypeName }]
                },
                "name": "PlayReady"
            },
            {
                "configuration": {
                    "@odata.type": "#Microsoft.Media.ContentKeyPolicyWidevineConfiguration",
                    "widevineTemplate": "{     \"allowed_track_types\": \"SD_HD\",     \"content_key_specs\": [         {             \"track_type\": \"SD\",             \"security_level\": 1,             \"required_output_protection\": {                 \"hdcp\": \"HDCP_NONE\",                 \"cgms_flags\": null             }         }     ],     \"policy_overrides\": {         \"can_play\": true,         \"can_persist\": true,         \"can_renew\": false,         \"rental_duration_seconds\": 2592000,         \"playback_duration_seconds\": 10800,         \"license_duration_seconds\": 604800     } }"
                },
                "restriction": {
                    "primaryVerificationKey": {
                        "@odata.type": "#Microsoft.Media.ContentKeyPolicySymmetricTokenKey",
                        "keyValue": params.contentKeyRestriction["PrimaryVerificationKey"]
                    },
                    "restrictionTokenType": "Jwt",
                    "@odata.type": "#Microsoft.Media.ContentKeyPolicyTokenRestriction",
                    "issuer": params.contentKeyRestriction["Issuer"],
                    "audience": audience,
                    "requiredClaims": [{ "claimType": customClaimTypeName }]
                },
                "name": "Widevine"
            }
        ] } }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-mkio-token": os.environ["MKIO_TOKEN"]
    }

    response = requests.patch(url, json=payload, headers=headers)

    print(response.text)

def main():
    if len(sys.argv) != 2:
        print("Usage: python contentkeypolicy_overwrite.py <environmentName: dev | qa | stage>")
        sys.exit(1)
    elif sys.argv[1] not in ["dev", "qa", "stage"]:
        print("Usage: python contentkeypolicy_overwrite.py <environmentName: dev | qa | stage>")
        sys.exit(1)

    environmentName = sys.argv[1]
    params = setEnvironmentParams(environmentName)
    overwriteContentKeyPolicy(params)

if __name__ == "__main__":
    main()