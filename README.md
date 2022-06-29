# Probably Genetic - Coding Challenge
See [challenge.md](challenge.md) for the challenge description.

## Solution

Hi! You can see the solution [here](http://ec2-52-88-42-74.us-west-2.compute.amazonaws.com:3000). Click on `symptoms` to see a page which allows you to search for symptoms, select them, and then compute the most likely diagnosis. Click on `disorders` to see a flat list of all the disorders available in the database.

### Edge Cases and Future Directions

- In the UI, make it more apparent why a particular disease was in the returned list, and give a probability estimate
- Use Machine Learning to build a better algorithm for computing the most likely diagnosis
- Use a proper database more suitable for large applications (Postgres, MySQL, etc.)
- Pull more descriptive data into the database from a third party API for each disorder
- Make the disorders and symptoms more searchable - use a search bar which leverages NLP for more approximate query matching
- Use caching to improve load times, especially since the data is relatively static
- Fix the favicon. Haven't figured out how to get it to refresh.
- Use a single `docker-compose` file for setup and deployment

## Run Unit Tests

`python3 -m pytest`

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
