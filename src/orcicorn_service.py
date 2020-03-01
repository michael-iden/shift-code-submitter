from apiron import Service, JsonEndpoint


class OrcicornService(Service):
    domain = 'https://shift.orcicorn.com/'

    bl3_codes = JsonEndpoint(
        path='/tags/borderlands3/index.json'
    )
