from apiron import Endpoint, Service


class ShiftCodeService(Service):
    domain = 'https://shift.gearboxsoftware.com'

    home = Endpoint(
        path='/home'
    )

    login = Endpoint(
        path='/sessions',
        default_method='POST'
    )

    check_code = Endpoint(
        path='/entitlement_offer_codes',
        required_params={'code'}
    )

    redeem_code = Endpoint(
        path='/code_redemptions',
        default_method='POST'
    )
