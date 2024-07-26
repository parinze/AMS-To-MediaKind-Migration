from collections import namedtuple

MKIO_API_URL_PREFIX = "https://api.mk.io/api/ams"

def setEnvironmentParams(environmentName: str):
    """
    Sets the environment parameters based on the environment name, given by a command line argument.

    Returns:
        selectedParams (namedtuple): environment, fileName, contentKeyRestriction, subscriptionName
            -environment (str): the name of the environment (de, qa, stage)
            -fileName (str): the name of the migration file
            -contentKeyRestriction (dict): the content key restriction information
                    -Issuer (str): the issuer
                    -PrimaryVerificationKey (str): the primary verification key
            -subscriptionName (str): the name of the subscription

    Parameters: 
        environmentName (str): the name of the environment (dev, qa, stage)
    """
    EnvironmentParams = namedtuple('EnvironmentParams', ["environment", "fileName", "contentKeyRestriction", "subscriptionName"])

    devQAContentKeyRestriction = {
        "Issuer": "https://test-platform-token-api.practicemgmt-test.pattersondevops.com/sts",
        "PrimaryVerificationKey": "ZjJaZitrbnFvZWxBbWpReXdVd2l2N2lTVzg1QjlrT3lZYVoxVHFJOA==",
    }

    stageContentKeyRestriction = {
        "Issuer": "https://stage-platform-token-api.practicemgmt-stage.pattersondevops.com/sts",
        "PrimaryVerificationKey": "RShIK01iUWVUaFdtWnE0dDd3IXolQypGKUpATmNSZlVqWG4ycjV1OHgvQT9EKEcrS2FQZFNnVmtZcDNzNnY5eQ==",
    }

    productionContentKeyRestriction = {
        "Issuer": "https://prod-pdco-platform-token-api.fuse.pattersondental.com/sts",
        "PrimaryVerificationKey": "dDZ3OXokQitFKUhATWNRZlRqV25acjR1N3ghQSVEKkYtSmFOZFJnVWtYcDJzNXY4eS9CP0UoSCtLYlBlU2hWbQ=="
    }

    devParams = EnvironmentParams(environment="dev", fileName="DEV_migration-1719511474.json", contentKeyRestriction=devQAContentKeyRestriction, subscriptionName="dolphmediasvc301_dev")
    qaParams = EnvironmentParams(environment="qa", fileName="QA_migration-1719513625.json", contentKeyRestriction=devQAContentKeyRestriction, subscriptionName="dolphmediasvc101_qa")
    stageParams = EnvironmentParams(environment="stage", fileName="STAGE_migration-1719514539.json", contentKeyRestriction=stageContentKeyRestriction, subscriptionName="dolphmediasvc201_stage")
    prodParams = EnvironmentParams(environment="prod", fileName="PROD_migration-1721748953.json", contentKeyRestriction=productionContentKeyRestriction, subscriptionName="dolphmediasvc001_prod")

    selectedParams = None

    if environmentName == "dev":
        selectedParams = devParams
    elif environmentName == "qa":
        selectedParams = qaParams
    elif environmentName == "stage":
        selectedParams = stageParams
    elif environmentName == "prod":
        selectedParams = prodParams
    else:
        raise ValueError("Invalid environment name. Please enter 'dev', 'qa', 'stage', or 'prod'.")

    return selectedParams
