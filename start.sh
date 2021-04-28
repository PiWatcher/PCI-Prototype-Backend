echo "Starting setup..."

echo "Is the environment DEV/PROD/TEST?"
read ENV

if [ $ENV = PROD ]
then
    echo "Setting up PROD environment..."
    
    # load prod environment variables
    . .env.prod
    sleep 1
    docker-compose --env-file .env.prod -f docker-compose.prod.yml up -d --build
    sleep 5
    docker exec mongodb-prod mongo -u $ROOT_USER -p $ROOT_PASS --eval "db.getSiblingDB('admin').createUser({user: '$MONGO_USER', pwd: '$MONGO_PASS', roles: ['readWriteAnyDatabase']});"
fi

if [ $ENV = DEV ]
then
    echo "Setting up DEV environment..."

    # load dev envrionment variables
    . .env.dev
    sleep 1
    docker-compose --env-file .env.dev up -d --build
    sleep 5
    docker exec mongodb-dev mongo -u $ROOT_USER -p $ROOT_PASS --eval "db.getSiblingDB('admin').createUser({user: '$MONGO_USER', pwd: '$MONGO_PASS', roles: ['readWriteAnyDatabase']});"
fi

if [ $ENV = TEST ]
then
    echo "Setting up TEST environment..."

    # load test environment variables
    . .env.test
    sleep 1
    docker-compose --env-file .env.test -f docker-compose.test.yml up -d --build
    sleep 5
    docker exec mongodb-test mongo -u $ROOT_USER -p $ROOT_PASS --eval "db.getSiblingDB('admin').createUser({user: '$MONGO_USER', pwd: '$MONGO_PASS', roles: ['root']});"
fi