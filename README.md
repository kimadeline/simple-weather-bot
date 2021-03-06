# Simple weather bot

Let's test the Python version of the Bot Framework SDK by building a simple bot that returns a short weather description whenever you enter a city. Additional steps include Azure deployment and Slack integration.

📺 A video-version of this tutorial can be found on [YouTube](https://www.youtube.com/watch?v=__ian1SZm78&list=PLlrxD0HtieHhQHeS5fjSHcdMeDTBRpVrU&index=5).

## Development

- Use Python 3.7, because Oryx (the build system) uses Python 3.7.9
- Sign up and get an API key on [OpenWeatherMap](https://openweathermap.org/api), store that key in a .env file at the workspace root
- Install [Bot Framework Emulator v4](https://github.com/microsoft/BotFramework-Emulator/blob/master/README.md)
- Move to the `weather_bot` folder
- Install all requirements: `python -m pip install -r requirements.txt`
- Check that the `cookiecutter` package was installed correctly by running `cookiecutter --help`
- Replace the placeholder OpenWeatherMap API key value in the .env file

## Local testing

- Run `python app.py` and remember the URL at which it's running
- Start the Bot Framework Emulator
- If no option to open a bot shows up, go to "File > Open Bot"
- Enter the bot URL and append `/api/messages`, should be something along the lines of `http://localhost:3978/api/messages`.
- Click "Connect" and you're set:

![Gif of testing the weather bot in the Bot Framework Emulator](./readme_assets/emulator.gif?raw=true)

## Deployment

These steps will deploy the bot to a new resource group. If you want to deploy to an existing resource group, refer to the [documentation](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-tutorial-deploy-basic-bot?view=azure-bot-service-4.0&tabs=python#deploy-via-arm-template-with-existing-resource-group).

### Local steps

1. Have the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) installed
1. Login to Azure: `az login`
1. Save your Azure subscription id from the output of the login command, or use `az account list`
1. Set the subscription to use for deploying the bot: `az account set --subscription "<azure-subscription-id>"`
1. Create an application registration: `az ad app create --display-name "displayName" --password "AtLeastSixteenCharacters_0" --available-to-other-tenants`
1. 🔐 Save the password and the `appId` (from the JSON output) somewhere
1. Run the first big scary command that will set up a bot application service on Azure for you:

```bash
az deployment sub create --template-file "<path/to/deploymentTemplates/template-with-new-rg.json>" --location <region-location-name> --parameters appId="<app-id-from-previous-step>" appSecret="<password-from-previous-step>" botId="<id or bot-app-service-name>" botSku=F0 newAppServicePlanName="<new-service-plan-name>" newWebAppName="<bot-app-service-name>" groupName="<new-group-name>" groupLocation="<region-location-name>" newAppServicePlanLocation="<region-location-name>" --name "<bot-app-service-name>"
```

Notes:

- F0 is the free tier plan
- Path to the template file: Absolute or relative to current directory
- Location: See `az account list-locations` and use the value of the `name` key (for example `westus2`)

While the setup command is running:

8. Create a zip file of your bot: Select all the files under the folder that contains the `app.py` file and package them. This also includes the .env file. Oryx will read the `requirements.txt` file and install the appropriate dependencies.
1. Run the not-so-big but still scary deployment command:

```bash
az webapp deployment source config-zip --resource-group "<resource-group-name>" --name "<name-of-web-app>" --src "<project-zip-path>"
```

10. If you want to check the deployment logs, run `az webapp log deployment show -n <name-of-web-app> -g <resource-group-name>` and click on the URL in the resulting JSON

### On the Azure portal

- Find the Bot Channels Registration entry for your bot
- In the side blade, select "Test using Web Chat" under the Settings category
- The interface is similar to the Bot Framework Emulator, which means that if the bot was deployed correctly, it should greet you, and reply to you whenever you enter a city:

![Gif of testing the weather bot in the Azure Portal Web Chat](./readme_assets/portal.gif?raw=true)

### Slack integration

The Microsoft Docs tutorial can be found [here](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-slack?view=azure-bot-service-4.0&tabs=abs).

There are 2 ways to connect your bot to Slack:

- Via the Azure Bot Service Portal (no code)
- With a Slack adapter (doesn't require tinkering with the Azure Portal, but can only be written in C# or JS)

We will go with the Azure Bot Service Portal solution.

Make sure you have permissions to deploy an app to the Slack workspace of your choice, check out this [Slack help center article](https://slack.com/help/articles/222386767-Manage-app-installation-settings-for-your-workspace) if you or your workspace owners need instructions on how to do so.

The steps pretty much follow the tutorial linked above:

- Create a Slack app on https://api.slack.com/apps
- Add https://slack.botframework.com as a redirect URL under "OAuth and Permissions"
- Go to "Event Subscriptions" and enable event subscription
  - Add `https://slack.botframework.com/api/events/<your-bot-handle>` as the request URL and replace with your bot handle, which can be found in your bot profile in the Azure Portal (Bot Channels Registration > Bot Profile)
  - Subscribe to bot events, the only ones we need here are `message.channels` and `message.im`
  - Remember to click on "Save Changes" ✅
- Get your Slack app credentials under "Basic Information" > "App Credentials"
- Go to the Azure Portal, create a Slack channel (might take a couple of retries if the page times out), paste the credentials
- It will open a pop-up window, accept your fate and authorize everything
- Bot is now in your workspace, you and anybody else in this workspace can talk to it in "Apps":

![Gif of testing the weather bot in Slack](./readme_assets/slack.gif?raw=true)

Note that this is for development purposes, and doesn't cover distributing the app in the Slack App Directory.
