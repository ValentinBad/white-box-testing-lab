from auth import authenticate_user

def test_missing_credentials():
    db = {}
    assert authenticate_user("", "pass", db) == "Missing credentials"
    assert authenticate_user("user", "", db) == "Missing credentials"

def test_user_not_found():
    db = {}
    assert authenticate_user("user", "pass", db) == "User not found"

def test_account_locked():
    db = {"user": {"password": "pass", "attempts": 3}}
    assert authenticate_user("user", "pass", db) == "Account locked"

def test_invalid_password():
    db = {"user": {"password": "pass", "attempts": 0}}
    assert authenticate_user("user", "wrong", db) == "Invalid password"
    assert db["user"]["attempts"] == 1

def test_success():
    db = {"user": {"password": "pass", "attempts": 1}}
    assert authenticate_user("user", "pass", db) == "Authenticated"
    assert db["user"]["attempts"] == 0


# 1. Обидва поля порожні ─ повна перевірка or‑умови (MC/DC, Comb.)
def test_both_username_and_password_missing():
    assert authenticate_user("", "", {}) == "Missing credentials"

# 2. Порожній тільки username
def test_only_username_missing():
    assert authenticate_user("", "pass", {}) == "Missing credentials"

# 3. Порожній тільки password
def test_only_password_missing():
    assert authenticate_user("user", "", {}) == "Missing credentials"

# 4. Невірний пароль, attempts < 3  → інкремент лічильника
def test_invalid_password_attempts_under_3():
    db = {"user": {"password": "correct", "attempts": 2}}
    assert authenticate_user("user", "wrong", db) == "Invalid password"
    assert db["user"]["attempts"] == 3          # лічильник зріс

# 5. Успішний логін із 0 спроб
def test_valid_user_zero_attempts():
    db = {"user": {"password": "pass", "attempts": 0}}
    assert authenticate_user("user", "pass", db) == "Authenticated"
    assert db["user"]["attempts"] == 0          # не змінюється

# 6. Успішний логін із ненульових спроб  → скидання лічильника
def test_valid_user_nonzero_attempts():
    db = {"user": {"password": "pass", "attempts": 2}}
    assert authenticate_user("user", "pass", db) == "Authenticated"
    assert db["user"]["attempts"] == 0          # скинулось
