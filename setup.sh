echo "Starting setup..."

echo "Is the environment DEV or PROD?"
read ENV

if [ $ENV = PROD ]
then
    echo "Setting up PROD environment..."
    
    # load prod environment variables
    . .env.prod
    docker-compose --env-file .env.prod up -f docker-compose.prod.yml up -d --build
else
    echo "Setting up DEV environment..."

    # load dev envrionment variables
    . .env.dev
    docker-compose --env-file .env.dev up -d --build
    sleep 1
    docker exec mongodb-dev mongo -u $ROOT_USER -p $ROOT_PASS --eval "db.getSiblingDB('admin').createUser({user: '$MONGO_USER', pwd: '$MONGO_PASS', roles: ['readWriteAnyDatabase']});"
fi

