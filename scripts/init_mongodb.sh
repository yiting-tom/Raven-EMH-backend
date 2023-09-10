#!/bin/bash

echo "Init mongodb"

mongo admin <<EOF 
db.createUser({ 
  user: '${MONGO_INITDB_ROOT_USERNAME}', 
  pwd: '${MONGO_INITDB_ROOT_PASSWORD}', 
  roles: [{role: 'root', db: 'admin'}]
}); 
db.shutdownServer();
EOF

echo "Init mongodb - Finished"
