from utils.password import hash_password, verify_password


class TestPassword:

    def test_hash_password(self):
        password = "password123"

        hashed_password = hash_password(password)

        assert hashed_password != password
        assert hashed_password is not None

    def test_verify_password(self):
        password = "password123"

        hashed_password = hash_password(password)

        assert verify_password(password, hashed_password) is True

    def test_wrong_password_fails(self):
        password = "password123"

        hashed_password = hash_password(password)

        assert verify_password("invalid password", hashed_password) is False