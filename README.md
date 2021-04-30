# Simple weather bot

Testing the Python version of the Bot Framework SDK by building a simple bot that returns a short weather description whenever you enter a city. Additional steps include Azure deployment and Slack integration.

Pictures/gifs would be nice.

## Development

- Use python 3.7, because Oryx (the build system) uses Python 3.7.9
- Install `pip-tools`
- Install [Bot Framework Emulator v4](https://github.com/microsoft/BotFramework-Emulator/blob/master/README.md)
- Sign up and get an API key on [OpenWeatherMap](https://openweathermap.org/api), store that key in a .env file at the workspace root
- Move to the `weather_bot` folder
- Install all requirements: `python -m pip install -r requirements.txt`
- Check that the `cookiecutter` package was installed correctly by running `cookiecutter --help`

## Local testing

- Run `python app.py` and remember the URL at which it's running
- Start the Bot Framework Emulator
- If no option to open a bot shows up, go to "File > Open Bot"
- Enter the bot URL and append `/api/messages`, should be something along the lines of `http://localhost:3978/api/messages`.
- Click "Connect" and you're set

## Deployment

These steps will deploy the bot to a new resource group. If you want to deploy to an existing resource group, refer to the [documentation]
(https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-tutorial-deploy-basic-bot?view=azure-bot-service-4.0&tabs=python#deploy-via-arm-template-with-existing-resource-group).

### Local steps

1. Have the Azure CLI installed
1. Know your azure subscription id: `az account list`
1. Login to azure: `az login`
1. Set the subscription to use for deploying the bot: `az account set --subscription "<azure-subscription-id>"`
1. Create an app registration: `az ad app create --display-name "displayName" --password "AtLeastSixteenCharacters_0" --available-to-other-tenants`
1. ⚠️ Save the password and the `appId` (from the JSON output) somewhere
1. Run the big scary deployment command:

```bash
az deployment sub create --template-file "<path/to/deploymentTemplates/template-with-new-rg.json>" --location <region-location-name> --parameters appId="<app-id-from-previous-step>" appSecret="<password-from-previous-step>" botId="<id or bot-app-service-name>" botSku=F0 newAppServicePlanName="<new-service-plan-name>" newWebAppName="<bot-app-service-name>" groupName="<new-group-name>" groupLocation="<region-location-name>" newAppServicePlanLocation="<region-location-name>" --name "<bot-app-service-name>"
```

Notes:

- F0 is the free tier plan
- Path to template file: Absolute or relative to current directory
- Location: See `az account list-locations` and use the value of the `name` key (for example `westus2`)

8. While that's running, create a zip file of your bot: Select all the files under the folder that contains the `app.py` file and package them. This means that if you use an env file, it should also be in this folder. Oryx will read the `requirements.txt` file and install the appropriate dependencies.
1. Run the not-so-big but still scary deployment command:

```bash
az webapp deployment source config-zip --resource-group "<resource-group-name>" --name "<name-of-web-app>" --src "<project-zip-path>"
```

10. If you want to check the deployment logs, run `az webapp log deployment show -n <name-of-web-app> -g <resource-group-name>` and click on the URL in the resulting JSON

### On the Azure portal

TODO with pictures
