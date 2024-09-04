from ..schema.auth import User

# 產生數個假的user_db
fake_users_db = {
    "johndoe": User(
        username="johndoe",
        full_name="John Doe",
        email="johndoe@example.com",
        hashed_password="$2b$12$KMLCEzogqHKsKcK6lii6MuP5qU/Xk3rIhT/X18yZzkfz7dj3Lwdyu",  # abcd
        disabled=False,
    ),
    "johndoe2": User(
        username="johndoe2",
        full_name="John Doe2",
        email="johndoe2@example.com",
        hashed_password="$2b$12$KMLCEzogqHKsKcK6lii6MuP5qU/Xk3rIhT/X18yZzkfz7dj3Lwdyu",  # abcd
        disabled=True,
    ),
}
