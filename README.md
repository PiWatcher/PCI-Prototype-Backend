# PCI Prototype Backend
This prototype provides a proof-of-concept (POC) and tests the feasibility of the technologies that we have chosen for our technological feasibility.

---

## Setup

1. Fork and Clone this project through HTTPS or SSH:

```
# Using HTTPS
git clone https://github.com/PiWatcher/PCI-Prototype-Backend.git

# Using SSH
git clone git@github.com:PiWatcher/PCI-Prototype-Backend.git
```

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

3. Once you have installed the required modules, the application is ready to be installed 

4. Ensure that you update the settings.py file with the correct configurations

### To test and start the server
```
python app.py
```

5. To setup and run the application within docker:

```
docker build -t piwatcher-backend:latest .
docker run -d -p 5000:5000 piwatcher-backend
```

You can check if the application is working by going to: localhost:5000/api