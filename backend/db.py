import os
import uuid

import pandas as pd
import traceback

CSV_FILE = "users.csv"
DASHBOARD_CSV = "dashboard.csv"


def load_users():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(
            columns=[
                "id",
                "email",
                "password",
                "verified",
                "token-verification",
                "first-access",
            ]
        )
        df.to_csv(CSV_FILE, index=False)
    return pd.read_csv(CSV_FILE)


def save_users(df):
    df.to_csv(CSV_FILE, index=False)


def user_exists(value, field="email"):
    df = load_users()
    return value in df[field].values


def change_cell(user_id, file, field, value):
    try:
        df = pd.read_csv(file)
        mask = df["id"] == user_id
        df.loc[mask, field] = value
        df.to_csv(file, index=False)
        return True
    except Exception:
        traceback.print_exc()
        return False


def verify_user_by_token(token):
    df = load_users()
    user = df[df["token-verification"] == token]

    if user.empty:
        return False, "User not found 😠"

    if user.iloc[0]["verified"]:
        return True, "Already verified 🤨"

    df.loc[df["token-verification"] == token, "verified"] = True
    save_users(df)
    return True, "Email verified successfully 🥳"


def check_credentials(email, password):
    df = load_users()
    user_row = df[df["email"] == email]
    if user_row.empty:
        return False, "Invalid User"
    if user_row.iloc[0]["password"] != password:
        return False, "Invalid Password"
    if not user_row.iloc[0]["verified"]:
        return False, "Email not verified"
    return True, "Login successful", user_row.iloc[0]


def add_user(email, password, token):
    df = load_users()
    new_id = str(uuid.uuid4())
    new_user = pd.DataFrame(
        [[new_id, email, password, False, token, False]],
        columns=["email", "password", "verified", "token-verification", "first-access"],
    )
    df = pd.concat([df, new_user], ignore_index=True)
    save_users(df)


def update_dashboard_db(data):
    try:
        # load or initialize dashboard CSV
        if os.path.exists(DASHBOARD_CSV):
            df = pd.read_csv(DASHBOARD_CSV)
        else:
            df = pd.DataFrame(
                columns=["id", "username", "date_of_birth", "gender", "avatar_id"]
            )

        user_row = df[df["id"] == data.get("id")]
        if not user_row.empty:
            return False
        # append new record
        new_record = pd.DataFrame(
            [
                {
                    "id": data.get("id"),
                    "username": data.get("username"),
                    "date_of_birth": data.get("date_of_birth"),
                    "gender": data.get("gender"),
                    "avatar_id": data.get("avatar_id"),
                }
            ]
        )
        df = pd.concat([df, new_record], ignore_index=True)

        # save back to CSV
        df.to_csv(DASHBOARD_CSV, index=False)
        return True
    except Exception:
        return False
