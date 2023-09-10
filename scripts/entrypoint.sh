#!/bin/bash

service mongodb start

sleep 5

init_mongodb.sh

make run
