from advanced_api_project.settings import *

# Use an in-memory SQLite database for testing
# This ensures tests run on a separate database that won't affect
# development or production data
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Using in-memory database for faster tests
    }
}

# Disable Django's caching during tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Disable password hashing to speed up tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable migrations when running tests
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Modify REST_FRAMEWORK settings for testing if needed
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}