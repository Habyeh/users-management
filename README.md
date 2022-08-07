# Users Management API v1.0.0

## Description
This API provides a mechanism to register users and their operations in the website, and allows to determine the difference (in days) between two given dates.

## Permissions
The authentication system has been based on SimpleJWT authentication.
When you login with the credentials of an existing user, the login endpoint return 2 tokens (access and refresh).
Access token must be in headers in order to authenticate the user, like the following:
'Authorization':'Bearer <access_token>'

## Format
All endpoints of this API receives and return data only in json format.

## Endpoints
Endpoints URLs and specifications are in: api/schema/swagger/

## Testing
Tests were developed using Pytest.
In order to test this API, open the project's main folder (with your virtual environment activated), and run 'pytest' in console.

## Running in local
If you want to run this code in local:
- Clone this repository.
- Change line 9 in manage.py file to:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings.development')
- Change line 14 in api/config/wsgi.py file to:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings.development')
- Enjoy.