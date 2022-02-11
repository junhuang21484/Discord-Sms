# Discord SMS Notification

A python script that help you send text message to your phone one
of your desire discord channel have a new message. The project is
built through the use of `Twilio` and `websocket`

## Installation
    1. Pip install requirements.txt
    2. Run main.py on your local machine/server

## Setup
The only thing that you need to change in order for main.py to run
properly is `setting.json` which will certain fields that you need
to input.

#### Sms Setting
    account_id - This is where you put your twilio account id
    auth_token - This is where you put your twilio auth token
    twilio_number - This is the phone number that shows up in your twilio account
    receiving_number - This is the phone number that you want the text msg send to

#### Discord Setting
    listen_channels - An array of channels where you want the discord listener listen to
    user_token - Your discord token

## Things to know
    - The script does not have any error handling currently
    - If the socket disconnect it will not reconnect
    - This project has not been heavily tested

## Todo List
    - Add embed support
    - Better documentations
    - Better socket handlings
    - Better error handlings

If you have any suggestions feel free to leave it!