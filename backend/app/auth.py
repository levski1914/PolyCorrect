import requests
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


SUPABASE_URL="https://uwjgaqhmsvinsagqnxkg.supabase.co"
SUPABASE_SERVICE_ROLE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3amdhcWhtc3ZpbnNhZ3FueGtnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NzkzMjA0MCwiZXhwIjoyMDYzNTA4MDQwfQ.iUwkwsE9clQsK3UHiZKl-J9UZ5vuc5xNaaYoc1dPx9A'


security=HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    user_info = response.json()
    return user_info["id"]