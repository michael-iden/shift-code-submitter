from bs4 import BeautifulSoup

from src.shift_code_service import ShiftCodeService
from src.user_builder import User

headers = {
    "x-csrf-token": "rvukLLRniU/Dbah6LwVT+bstmhe6garMIWyHpNGmkPdKIUS/9XVZnraqPlRDqy4n7A6JrUE4q4jSehaG5W6fDg==",
    "dnt": "1",
    "x-requested-with": "XMLHttpRequest"
}


class ShiftCodeClient:

    def __init__(self, user: User, shift_code: str) -> None:
        self.user = user
        self.shift_code = shift_code
        self.session_id = None
        self.session_token = None

    @property
    def session_cookies(self):
        return {
            "_session_id": self.session_id,
            "si": self.session_token
        }

    def submit_shift_code(self):
        self.__login()

        check_code_response = ShiftCodeService.check_code(
            params={'code': self.shift_code},
            headers=headers,
            cookies=self.session_cookies,
            allow_redirects=False
        )
        parsed_check_response = BeautifulSoup(check_code_response)

        form_data = self.__build_redemption_form_data(parsed_check_response)
        redemption_response = ShiftCodeService.redeem_code(
            data=form_data,
            headers={'dnt': '1', "Referer": f"{ShiftCodeService.domain}/rewards"},
            cookies=self.session_cookies
        )

        # parsed_redemption_response = BeautifulSoup(redemption_response)
        # if 'Failed to redeem your SHiFT code' in parsed_redemption_response.find("div", {"class": "alert notice"}).text:
        #     raise Exception(f'Unable to redeem code for {self.user.name}')

    def __login(self):
        raw_homepage_response = ShiftCodeService.home(return_raw_response_object=True)
        parsed_homepage_response = BeautifulSoup(raw_homepage_response.text)

        initial_session_cookie = raw_homepage_response.cookies.get('_session_id')
        login_form_data = self.__build_login_form_data(parsed_homepage_response)
        raw_login_response = ShiftCodeService.login(
            data=login_form_data,
            cookies={"_session_id": initial_session_cookie},
            return_raw_response_object=True,
            allow_redirects=False
        )
        if '/account' in raw_login_response.text:
            self.session_id = raw_login_response.cookies.get('_session_id')
            self.session_token = raw_login_response.cookies.get('si')

    def __build_login_form_data(self, parsed_homepage_response):
        return {
            'utf8': '&#x2713;',
            'authenticity_token': parsed_homepage_response.find("input", {"name": "authenticity_token"}).get('value'),
            'user[email]': self.user.email,
            'user[password]': self.user.password,
            'commit': 'SIGN IN'
        }

    def __build_redemption_form_data(self, parsed_check_response):
        return {
            'utf8': '&#x2713;',
            'authenticity_token': parsed_check_response.find("input", {"name": "authenticity_token"}).get('value'),
            'archway_code_redemption[code]': parsed_check_response.find("input", {"id": "archway_code_redemption_code"}).get('value'),
            'archway_code_redemption[check]': parsed_check_response.find("input", {"id": "archway_code_redemption_check"}).get('value'),
            'archway_code_redemption[service]': 'epic',
            'archway_code_redemption[title]': parsed_check_response.find("input", {"id": "archway_code_redemption_title"}).get('value'),
        }

