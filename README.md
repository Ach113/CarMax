## CarMax
CarMax, a chatbot written using RASA 3.3.1

## Requirements
rasa >= 3.3.1 \
tensorflow >= 3.8.3 \
bs4 >= 4.11.1 \
pandas >= 1.5.1 \
uszipcode >= 1.0.1

## How to run
Clone the repository and install dependencies \
`git clone https://github.com/Ach113/CarMax` \
`cd CarMax` \
`pip install -r requirements.txt`

Setup server side (connect to slack) \
`rasa run` \
`rasa run actions`

You can use [ngrok](https://ngrok.com/download) to deploy the chatbot on slack \
`ngrok http 5005` 

Finally, run the commands

## Example commands

### Database lookup 
`$>  I'm looking for Chevrolet` \
Found 296 instances of chevrolet, please enter you zip code so we can find a car closest to you \
`$>  95112` \
Found cheapest car - chevrolet at price of 3000$. 
You can check the vehicle using this vin: 1gccsbf92c8121126 

### Web lookup
`$> I want to buy Honda Civic` \
Honda Civic could not be found in our database. Please try again if you made a typo, or type `search on web` if you want to search the car outside of our database. \
`$> search on web` \
I can help you with that. What kind of car are you looking for? \
`$> I'm looking for Honda Civic` \
Found honda civic with lowest price (6490$) at https://www.cars.com/vehicledetail/73a9e547-e5b8-40a8-8300-946f88e2e830/






