
| Travis        | AppVeyor      |
|:-------------:|:-------------:|
| [![Build Status](https://travis-ci.org/oefsv/ulti-players.svg?branch=master)](https://travis-ci.org/oefsv/ulti-players) | - |

# Test

You need to install
+ python
+ yarn


To start the dev server for the UI, use:
```
> gradlew :frontend:startUi
```
In order to initialize the backend server, use
```
> gradlew :backend:initDev
```
The first time, you might need to create the admin user
```
> cd backend
> frisbee-venv\Scripts\python.exe manage.py createsuperuser
```
Start the dev server using
```
> frisbee-venv\Scripts\python.exe backend\manage.py runserver
```

# Develop

## UI

UI development is done using Angular + Yarn
```
> cd frontend
> yarn install
> yarn start
```

# Build
Create the ZIP
```
> gradlew createZip
```


