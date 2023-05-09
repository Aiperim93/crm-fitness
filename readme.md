# A CRM system for a fitness platform with a Telegram bot.

### This CRM system is a solution for managing clients, trainers, and their workouts on a fitness platform. The functionality is available both through a web interface, implemented on the __Django__ framework, and through a Telegram bot implemented using the __Aiogram__ library.
#### Key features:

Accounting for clients, trainers, workouts, payments, and freezes
Ability to view the training and payment history of clients
Notification of clients through a Telegram bot, as well as through the web interface.

#### "How to launch the project:
Clone the repository and navigate to the project's source folder.
The program is written using Docker and Docker-compose, so there is no need to install additional dependencies.
Migrations are configured to run during the startup of the Docker container.
You only need to build the container using the command docker-compose up --build.
To launch the Telegram bot, you need to be in the tg_bot folder and start the bot using the command docker-compose run bot."


#### "How to use the Telegram bot:
To make the Telegram bot available to the admin, add the admin's Telegram ID in the Django admin panel.
Add the Telegram bot t.me/esdp_fitnessBot to your account and to the clients' accounts as well.
Send the command /start to the bot to begin interacting with it.
Receive notifications about new workouts, mailings, and promotions."

####  Documentation [here.](documentation.md)

___

#### 
MEDERBEKOVA AIPERIM @aiperim93 
