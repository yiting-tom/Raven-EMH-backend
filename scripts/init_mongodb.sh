#!/bin/bash

echo "Init mongodb"

set -e

service mongodb start

mongo admin <<EOF 
db.createUser({ 
  user: '${MONGO_INITDB_ROOT_USERNAME}', 
  pwd: '${MONGO_INITDB_ROOT_PASSWORD}', 
  roles: [{role: 'root', db: 'admin'}]
}); 
EOF

echo "Init mongodb - Finished"
