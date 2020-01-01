# ai_python_bot

<h1>Telegram Bot with Artificial intelligence</h1> 
<h2>(30 lines of Python)</h2>
<br>
<h3>So, to create a telegram chat-bot with AI all we need is:</h3>

<ol>
<li>Telegram API. As a wrapper, I took a proven library of <a href="https://github.com/python-telegram-bot/python-telegram-bot">python-telegram-bot</a></li>
<li>API AI. I chose a product from Google, specifically <a href="https://dialogflow.com/">Dialogflow</a>. It provides a fairly good free API. <a href="https://github.com/dialogflow/dialogflow-python-client">The Dialogflow wrapper for Python</a></li>
</ol>

<h3>Step 1. Let's create a bot in Telegram</h3>
<p>We choose a name and send it to <a href="https://t.me/botfather">@botfather<a/>. After the creation of the bot, we will get the API Token, save it somewhere, since in the future we will need it.</p>
<img src="https://raw.githubusercontent.com/millennium-salander/ai_python_bot/master/img/1_bot.png" width="450"/>

<h3>Step 2. Let's write the basics of our bot</h3>
<p>Create a folder named "Bot", in which then create the bot.py file. Here will be the code of our bot.
Open the console and go to the directory with the file, install <strong>python-telegram-bot</strong>.</p>
<h6>pip install python-telegram-bot --upgrade</h6>
<p>After the installation, we can already write the "basics", which for now will simply respond with the same type of messages. Let's import the necessary modules and register our API token:</p>

```python
# Settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
updater = Updater(token='YOURE API TOKEN') # Telegram API Token
dispatcher = updater.dispatcher
```
<p>Next, we write 2 command handlers. These are callback functions that will be called when the update is received. Let's write two such functions for the <strong>/ start</strong> command and for any plain text message. Two parameters are passed there as arguments: <strong>bot</strong> and <strong>update</strong>. <strong>Bot</strong> contains the necessary methods for interacting with the API, and <strong>update</strong> contains information about the incoming message.</p>

```python
# Command processing
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello, do you want to talk?')
def textMessage(bot, update):
    response = 'Got youre message: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)
```

<p>Now all we need is to assign these handlers to notifications and start searching for updates.
This is done very simply:</p>

```python
# Handlers
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Here we add the handlers to the dispatcher
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Start search for updates
updater.start_polling(clean=True)
# Stop the bot, if Ctrl + C were pressed
updater.idle()
```

<p>Now we can test the performance of our new bot. Let's paste our API token on line 2, then save the changes, move it to the console and run the bot:</p>
<h6>python bot.py</h6>

<p>After the start send him a message. If everything were done correctly you will see this:</p>
<img src="https://raw.githubusercontent.com/millennium-salander/ai_python_bot/master/img/bot_2.png" width="450"/>
<p>The basiscs for the bot are written, let's proceed to the next step!<br>
P.s. do not forget to turn off the bot. To do that go back to the console and press Ctrl + C, wait a couple of seconds and the bot will successfully complete the work.</p>


<h3>Step 3 AI Settings</h3>
<p>First of all, sing up on Dialogflow (just log in with your Google account). Immediately after the authorization, we get to the control panel.</p>
<img src="https://raw.githubusercontent.com/millennium-salander/ai_python_bot/master/img/bot_3.png" width="650"/>
<p>Click on <strong>Create Agent</strong> and fill in the fields with you're with whatever you want (this will not play any role, it is only necessary for the next action).<br> After that click on <strong>Create</strong>.</p>
<img src="https://raw.githubusercontent.com/millennium-salander/ai_python_bot/master/img/bot_4.png" width="650"/>

<p>Now i will tell you why the "Agent" that we created earlier does not play any role. In the Intents tab, there are "commands" on which the bot works. Now he can only respond to phrases such as "Hello", and if he does not understand, he answers "I did not understand you". Not very impressive.
After creating our empty agent, we have a bunch of other tabs. We need to click on Prebuilt Agents (these are already specially trained agents that have many commands) and select Small Talk from the entire list. </p>
<img src="https://raw.githubusercontent.com/millennium-salander/ai_python_bot/master/img/bot_5.png" width="650"/>

<p>Click on <strong>Import</strong>. Then, without changing anything click on <strong>Ok</strong>. The agent was imported and now we can configure it. To do this, in the upper left corner click on the gear near the Small-Talk and get to the settings page. Now we can change the agent's name as desired (I leave it as it was). We change the time zone and in the Languages tab we make sure that the English language has been set.</p>
<img src="https://raw.githubusercontent.com/millennium-salander/ai_python_bot/master/img/bot_6.png" width="650"/>

<p>Now we go back in <strong>General</strong> and copy the <strong>Client acess token</strong></p>
<img src="https://raw.githubusercontent.com/millennium-salander/ai_python_bot/master/img/bot_7.png" width="650"/>

<p>Now that our AI is completly ready we can go back to the bot</p>

<h3>Step 4. Let's put it all together</h3>
<p>AI is ready, bot basics are ready, what's next?</p>
<br>
<p>Next, we need to download the API wrapper from Dialogflow for python.</p>
<h6>pip install apiai</h6>
<p>Perfect. Now let's go back to our bot.</p>
<br>
<p>Let's add to our "Settings" section the import of apiai and json modules (you need to disassemble the responses from dialogflow in the future). Now it looks like this:</p>

```python
# Settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='YOURE API KEY') # Telegram API Token
dispatcher = updater.dispatcher
```

<p>Go to the function <strong>textMessage</strong> (which is responsible for receiving any text message) and send the received messages to the Dialogflow server:</p>

```python
def textMessage(bot, update):
    request = apiai.ApiAI('YOURE API TOKEN').text_request() # Dialogflow API Token
    request.lang = 'en' 
    request.session_id = 'YoureBot' # ID dialog session (for bot training)
    request.query = update.message.text # Send request to AI with the user message
```

<p>This code will send a request to Dialogflow, but we also need to extract the answer. After adding a couple of lines the <strong>textMessage</strong> looks like this:</p>

```python
def textMessage(bot, update):
    request = apiai.ApiAI('YOURE API TOKEN').text_request() # Dialogflow API Toke
    request.lang = 'en' 
    request.session_id = 'BatlabAIBot' # ID dialog session (for bot training)
    request.query = update.message.text # Send request to AI with the user message
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Take JSON answer
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='I dont understand!')

```
<p><strong>Some explanations</strong>:</p>
<h6>request.getresponse().read()</h6>
<p>get the response from the server, encoded in bytes. To decode it, we simply apply the method:</p>
<h6>decode('utf-8')</h6>
<p>And after that we "wrap" everything in:</p>
<h6>json.loads()</h6>

<p>Now all you need is ti save everything and check the bot</p>
<img src="https://raw.githubusercontent.com/millennium-salander/ai_python_bot/master/img/bot_8.png" width="450"/>

<h3>Step 5.</h3>
<p>It took us 10 minutes to create our first AI bot. Of course it still need some massive training. You can do it in the section <strong>Training</strong> on Dialogflow.</p>

<p>Now if you want to host youre bot you can use the <a href "https://github.com/millennium-salander/heroku-telegram-bot">Where to host Telegram Bots</a> guide.</p>

