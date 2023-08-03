# Roadmap for card_pay_emulator project

This is a microservice that represents payments system. so, 
it can registers cards, check balance and perform money transactions
it is needed to provide need a basic auth system

## v 0.1.0
Stories:

#### register
As an anon user
i want ask to register my app
and receive token to access functionality

#### trust request
As an auth user
i want to request access to info about untrusted card
and be granted with access or receive denition message

#### transaction
As an auth user
i want to request transaction from trusted card A to trusted card B
and receive status of transaction

#### reliability
As an auth user
i want to make transaction
and be sure that it was atomic


## SETUP PROJECT
#### Install dependencies
1) `python -m venv venv`
2) `source venv/bin/activate`
3) `pip install -r requirements.txt`

#### Init project database
1) init database - `alembic upgrade head`
2) create .env file - `cp .env.example .env`

#### launch server
1) uvicorn service.endpoints:app --port 8002 --reload --log-config ./log.ini
2) access web app at http://localhost:8002
