#!/bin/bash

# Need to figure out how to retrive api key

sqlite3 OmbiSettings.db "SELECT Content FROM GlobalSettings WHERE Id=1"

curl --location --request POST 'http://ombi:3579/api/v1/Job/arrAvailability' --header 'ApiKey: <OMBI API>' --header 'Content-Length: 0'