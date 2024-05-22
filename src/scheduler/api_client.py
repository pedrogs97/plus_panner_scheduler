from typing import Optional
from datetime import datetime
import requests
from src.config import INVERTEXTO_TOKEN, CORE_API_URL, CORE_KEY
from src.scheduler.models import HolidayModel
from src.enums import Ufs

class APIClient:
    """API Client"""

    def __init__(self):
        if not INVERTEXTO_TOKEN:
            raise ValueError("INVERTEXTO_TOKEN not set")

        if not CORE_API_URL:
            raise ValueError("CORE_API_URL not set")

        if not CORE_KEY:
            raise ValueError("CORE_KEY not set")

    async def __save_holidays(self, holidays: dict) -> None:
        """Save holidays in the database"""
        await HolidayModel.create(
            **holidays,
            date=datetime.strptime(holidays["date"], "%Y-%m-%d")
        )

    def get_current_year_holidays(self, state: Optional[Ufs] = None) -> bool:
        """Get current year holidays"""
        try:
            current_year = datetime.now().year
            url = f"https://api.invertexto.com/v1/holidays/{current_year}"
            if state:
                url += f"?state={state.value}"
            headers = {"Authorization": f"Bearer {INVERTEXTO_TOKEN}"}
            response = requests.get(url, headers=headers, timeout=500)
            success = response.status_code == 200
            if success:
                self.__save_holidays(response.json())
            return success
        except Exception: # pylint: disable=broad-except
            return False

    def check_if_clinic_exist(self, clinic_id: int) -> bool:
        """Check if clinic exists"""
        url = f"{CORE_API_URL}/clinics/{clinic_id}/check/"
        headers = {"X-API-Key": CORE_KEY}
        response = requests.get(url, headers=headers, timeout=500)
        return response.status_code == 200 and response.json()

    def check_if_desk_exist(self, desk_id: int) -> bool:
        """Check if desk exists"""
        url = f"{CORE_API_URL}/desks/{desk_id}/check/"
        headers = {"X-API-Key": CORE_KEY}
        response = requests.get(url, headers=headers, timeout=500)
        return response.status_code == 200 and response.json()

    def check_if_desk_vacancy(self, desk_id: int) -> bool:
        """Check if desk vacancy"""
        url = f"{CORE_API_URL}/desks/{desk_id}/vacancy/"
        headers = {"X-API-Key": CORE_KEY}
        response = requests.get(url, headers=headers, timeout=500)
        return response.status_code == 200 and response.json()

    def check_is_token_is_valid(self, token: str) -> bool:
        """Check if token is valid"""
        url = f"{CORE_API_URL}/auth/check-token/"
        headers = {"X-API-Key": CORE_KEY, "Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers, timeout=500)
        return response.status_code == 200 and response.json()