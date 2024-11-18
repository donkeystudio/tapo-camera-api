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

```json
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
* Request method: GET
* URL: http://0.0.0.0:5020/privacy
* Request body:
  * `host`: Optional. Without request body, status of all cameras will be returned.

#### Request example
```json
{
  "host":"C200_ABCDEFG"
}
```

#### Response example
```json
{
  "data": [
    {
      "host": "C200_ABCDEFG",
      "privacy_enabled": true,
      "name": "Foyer"
    }
  ],
  "status": "OK"
}
```

### Enable or disable privacy statuses
* Request method: `POST`
* URL: http://0.0.0.0:5020/privacy
* Request body:
  * `privacy`: true/false. Required.
  * `host`: Optional. Enable/Disable all cameras if not passed.

#### Request examples
##### Enable privacy mode
```json
{
  "privacy": true,
  "host":"C200_ABCDEFG"
}
```

##### Disable privacy mode

```json
{
  "privacy": false,
  "host":"C200_ABCDEFG"
}
```

#### Response example
```json
{
  "data": [
    {
      "host": "C200_ABCDEFG",
      "privacy_enabled": true,
      "name": "Foyer"
    }
  ],
  "status": "OK"
}
```

