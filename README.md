# Hot-Car-Data-Collection
A set of scripts to help collect data for our Third Year design project

## Requirements

* Python 3

## Setup

```
pip install https://github.com/adafruit/Adafruit_Python_DHT/archive/master.zip
pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Running

If you don't already have a database initialized, you will have to run the following:

```
python ./session_recorder.py initdb
```

The easiest way to start a data collection is to run the command with no parameters. It will prompt you to enter the session information.
```
python ./session_recorder.py record
```

You'll get the following output:
```
What type of subject? (none/adult/child/pet) [adult]: child
What is the car id? [1]: 1
```

However, if you would like to put the information in as command line arguments, that's also possible:


```
python ./session_recorder.py record --subject-type adult --car-id 1
```

You can find help about the command line arguments with:

```
python ./session_recorder.py <command_name> --help
```
