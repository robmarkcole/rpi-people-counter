#!/bin/bash

# Remember to start the MongoDB database (mongod) and the MQTT server (mosquitto).

# Start the data listener
echo "Starting client server..."
cd client
# cd ~/deploy-folder/client
npm run watch
# node browserSync.js
