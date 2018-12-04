#iReporter [![Build Status](https://travis-ci.com/ValerieRono/ireporter.svg?branch=develop)](https://travis-ci.com/ValerieRono/ireporter) [![Coverage Status](https://coveralls.io/repos/github/ValerieRono/ireporter/badge.svg?branch=bg-fix-endpoints-output-format)](https://coveralls.io/github/ValerieRono/ireporter?branch=bg-fix-endpoints-output-format)

#IREPORTER

A RESTFUL citizen-reporting api built on Python Flask that allows users to report incidences that need interventions from the government or that people need to be aware of(red flag records).

This is deployed on HEROKU : https://ireporter-valerie.herokuapp.com/api/v1/incidents


##Prerequisites 

To run the app, you need to install a couple of dependencies. Check the requirements.txt file to see the dependencies. See below for detailed guidelines

#Getting Started - installation guide


These are instructions on how to set up the application on a local development machine.

-Clone the repository
----git clone https://github.com/ValerieRono/ireporter.git
-Set up the virtual environment
----source venv/bin/activate
Install the dependencies
----pip install -r requirements.txt
Run the application
----flask run
Once you run the app, the default port for flask api is 5000, so use the following link to test the app on postman:(append to the url depending on method you want to test, see below)
----http://localhost:5000

The api has endpoints for:

creation of red flag records - /api/v1/incidents

viewing red flag records - /api/v1/incidents

viewing a specific red flag record - /api/v1/incidents/<int:id>

editing a red flag record - /api/v1/incidents/<int:id>

deleting a red flag record - /api/v1/incidents/<int:id>

where <int:id> is replaced by the id of the record you want to manipulate expressed as an interger

#Running the tests


using pytest
In the root directory of the application, run the following command
----`pytest`

#Deployment


Click on the link provided above to deploy the app to HEROKU

#Built with


Python 2.7.15
Flask 1.0.2
Pytests

#contributing


Anyone is free to contribute to the project

#versioning


We use [Blueprints](https://sanic.readthedocs.io/en/latest/sanic/blueprints.html) for versioning

#authors


Valerie Rono

#licence


This project is licensed under the MIT License - see the LICENSE.md file for details

#acknowledgements


I would like to express my gratitude to ANDELA, our learning facillitators and our teeammates for the mentorship and tutoring as we learnt and implemented this project


