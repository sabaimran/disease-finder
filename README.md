# Probably Genetic - Coding Challenge
See [challenge.md](challenge.md) for the challenge description.

## Solution

Hi! You can see the solution [here](http://ec2-52-88-42-74.us-west-2.compute.amazonaws.com:3000). Click on `symptoms` to see a page which allows you to search for symptoms, select them, and then compute the most likely diagnosis. Click on `disorders` to see a flat list of all the disorders available in the database.

## Local Development

### If using Docker Compose (preferred)

#### Prerequisites
- `sudo apt install docker-compose` ; Ensure you have docker-compose installed.

Open two separate terminals, one to run the server and one to run the client.

#### Run the client
`cd disease-finder/client && docker-compose up`

#### Run the server
`cd disease-finder/server && docker-compose up`

### If using local development (for Ubuntu 22.04)

#### Prerequisites
- `node --version` > v16.15.1
- `yarn --version` > v1.22.15
- `sudo apt install python3.10-venv` # Ensure you have python3.10-venv installed to properly setup the virtual environment.

#### Run the client
1. `yarn install`
2. `yarn start`

#### Run the server

1. `chmod +x run.bash`
2. `./run.bash`

If you're testing in this way and need to re-start the server, please comment out the db initialization step in `run.bash` to save yourself 30 minutes 😊.

## Stack
- React - frontend
- Flask - API
- sqlite - database
- SQLAlchemy - ORM
