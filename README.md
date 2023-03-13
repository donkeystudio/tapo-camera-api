# Tapo camera API

HTTP JSON API for viewing and controlling Tapo camera's privacy mode.

## Prequisites

* Python 3.9 or later
* pip

### Install dependencies

`pip install -r requirements`

## Configuring application

The application needs to be configured so that it knows what cameras it should interact with.
[Configuration template](config.json) is provided. The configuration is set so that all cameras must have the same local credentials.

### Example configuration

```Javascript
{
  "user": "camera_local_user",
  "password": "password",
  "hosts": [
    {
      "host": "C200_ABCDEFG",
      "name": "Foyer"
    }
  ]
}
```

## Run application

With the default configuration file

`python tapo_camera_api.py`

or with a custom configuration file

`python tapo_camera_api.py my_configuration.json`

## Endpoints

### List camera privacy statuses

Request method: GET
URL: http://0.0.0.0:5020/privacy

#### Response example

```Javascript
{
  "data": [
    {
      "host": "C200_ABCDEFG",
      "privacy_enabled": true,
      "name": "Foyer"
    }
  ]
  status": "OK"
}
```

### Enable or disable privacy statuses

Request method: POST
URL: http://0.0.0.0:5020/privacy

#### Request examples

##### Enable privacy mode

```Javascript
{
  "privacy": true
}
```

##### Disable privacy mode

```Javascript
{
  "privacy": false
}
```

#### Response example

```Javascript
{
  "data": [
    {
      "host": "C200_ABCDEFG",
      "privacy_enabled": true,
      "name": "Foyer"
    }
  ]
  status": "OK"
}
```

