# PCI Backend
This codebase serves as the backend to our web application of the People Counting Infrastructure. Down below is the setup instructions for starting development.

---

## Setup

1. To start development, fork and clone this project through HTTPS or SSH:

```
# Using HTTPS
git clone https://github.com/PiWatcher/PCI-Prototype-Backend.git

# Using SSH
git clone git@github.com:PiWatcher/PCI-Prototype-Backend.git
```

Side note: If you setting this up in a production environment, download the release,
and skips steps 1 and 2.

2. Setup your workstation for local development by creating a virtual environment and installing project dependencies:

### For Windows:
```
# Make sure pip is installed
python -m pip --version

# Install virtualenv
python -m pip install --user virtualenv

# Create the virtual environment
python -m virtualenv env

# Activate the virtual environment
.\env\Scripts\activate

# Confirm you are in the virtual environment
where python

# Install project dependencies
pip install -r requirements.txt
```

### For macOS and Linux:
```
# Make sure pip is installed
pip --version

# Or
pip3 --version

# Install virtualenv
python3 -m pip install --user virtualenv

# Create the virtual environment
python3 -m virtualenv env

# Activate the virtual environment
source env/bin/activate

# Confirm you are in the virtual environment
which python

# Install project dependencies
pip install -r requirements.txt
```

**Whenever you are developing locally, ensure that your virtual environment is activated or you will not have the valid project dependencies!**

You can leave the virtual environment by running in your CLI:
```
deactivate
```

3. Once you have installed the required modules, the application is ready to be installed.

4. To setup and run the application within docker:

First, run this command to ignore all changes that is going to be made in this file
```
git update-index --assume-unchanged .env.dev
git update-index --assume-unchanged .env.prod
git update-index --assume-unchanged .env.test
```

Then add environment variables for MONGO_USER, MONGO_PASS, ROOT_USER, ROOT_PASS, JWT_SECRET_KEY.

If you downloaded the application as a release, skip the git commands and just update
.env.* files.

From here, the application should be setup and ready to go.

Feel free to compose the docker container and run it by using the following command:
```
./start.sh
```

The start.sh file will ask for which environment you want to setup the application for.
Pick which one for you needs.

You can check if the application is working by going to: localhost:5000/api

6. To completely clean Docker instances:

```
docker system prune -a
docker volume prune -a # this will delete all data from the mongo database
```