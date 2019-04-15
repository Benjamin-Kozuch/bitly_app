# Bitly API (allow user to see average click traffic per country)

## Install & Run

```
git clone 
docker build -t bitly_app:latest .
docker images  # Should have python and bitly_app images
docker run --name bitly_app -p 80:5000 --rm \
-e ACCESS_TOKEN=change-this-to-your-access-token \
bitly_app:latest
```

## Endpoints

LOCALHOST
```
localhost/avg_clicks_per_country
localhost/avg_clicks_per_country/<your-access-token>
```
if you leave out `your-access-token` then the app will use the access-token stored in an environment variable (mine)

LIVE DEMO (deployed to ec2 using docker)
```
http://ec2-18-237-78-24.us-west-2.compute.amazonaws.com/avg_clicks_per_country
http://ec2-18-237-78-24.us-west-2.compute.amazonaws.com/avg_clicks_per_country/<your-access-token>
```

Try puting in your access token to see your average by country!


## Design decisions

The goal here, if I understand correctly, is to expose an API which return a list of all the countries and for each country, the average number of clicks for all bitlinks clicked from that country.

For example:

Lets say we have US, Canada and UK as our 3 countries. And me have 2 Bitlinks (bitlink A and bitlink B).

COUNTRY | Bitlink A | Bitlink B
--- | --- | --- 
US  |  4  |  8
CA  |  1  |  5
UK  |  0  |  10

```
US -> (4+8) / (total bitlinks clicked) -> (4+8)/2 = 6
CA -> (1+5) / (total bitlinks clicked) -> (1+5)/2 = 3
UK -> (10) / (total bitlinks clicked) -> (10)/1 = 10
```

Our API should return:
```
.
.
.
"metrics": [
    {
    "average_clicks": 6,
    "value": "US"
    },
    {
    "average_clicks": 3,
    "value": "CA"
    },
    {
    "average_clicks": 10,
    "value": "UK"
    }
.
.
],
```

In the case of UK above, I wasn't sure whether the calculation should be

UK -> (10) / (total bitlinks clicked) -> (10)/1 = 10

OR

UK -> (10) / (total bitlinks clicked) -> (0+10)/2 = 5

There are pros and cons to each of these approaches.

On the one hand, if we include UK/Bitlink A in the calculation it skewing the data with a country which obviously had no interaction with this link. Meaning, there are many other countries that also didn't click on this list and we are not including them in the calculation.

One the other hand. The UK did click on some of our other links so in that way it would make sense to include them in the calculation even for a bitlink which they didnt click on at all.

I decided to go with the former and if a country had Zero interaction with a certain Bitlink, then I am not going to include them at all in the average. I chose this because if I was the consumer of this data, it would be more interesting to me to get the average clicks  of the countries that at least had SOME interaction with that bitlink.

So my approach is going to be to keep a dictionary of the running sums of all the clicks per country and also the number of countries that clicked on that bitlink. Then I will do the division and create the response.

So after looping through all my bitlinks and getting the clicks per country of each bitlink I should have a dict that looks like this:

```
"CA": [
    1,
    5
],
"GB": [
    10
],
"US": [
    4,
    8
]
```

After that, its just a matter of summing up all the clicks in each list and dividing by the total elements in that list to end up with something like this:

```
"metrics": [
    {
    "average_clicks": 6,
    "value": "US"
    },
    {
    "average_clicks": 10,
    "value": "GB"
    },
    {
    "average_clicks": 3,
    "value": "CA"
    }
]
```

For my own exploratory purposes I used https://www.tunnelbear.com/ to 'fake' clicking on bitlinks from different countries.


## Run test.py

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python tests.py
```
