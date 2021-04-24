# Development

- Install `pip-tools`
- Install [Bot Framework Emulator v4](https://github.com/microsoft/BotFramework-Emulator/blob/master/README.md)
- Sign up and get an API key on [OpenWeatherMap](https://openweathermap.org/api), store that key in a .env file at the workspace root
- Move to the `weather_bot` folder
- Install all requirements: `python -m pip install -r requirements.txt`
- Check that the `cookiecutter` package was installed correctly by running `cookiecutter --help`

# Local testing

- Run `python app.py` and remember the URL at which it's running
- Start the Bot Framework Emulator
- If no option to open a bot shows up, go to "File > Open Bot"
- Enter the bot URL and append `/api/messages`, should be something along the lines of `http://localhost:3978/api/messages`.
- Click "Connect" and you're set

# Deployment

- Login to azure: `az login`
