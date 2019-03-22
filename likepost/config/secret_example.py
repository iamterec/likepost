DATABASE_USER = "test_user"
DATABASE_PASSWORD = "test_password"


class SecretConfig:
    SECRET_KEY = 'GLEWR2hivpEK7y4Kk35A1vmTLfXM6no0a5yAYhAJ'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@postgres:5432/likepost'\
        .format(DATABASE_USER, DATABASE_PASSWORD)
    JWT_SECRET_KEY = 'TXMLoOpl2UOIPOdcjziBccKQyMxss9hHG74HnhkY'
