import platform
from getpass import getuser


def get_client_details():
    """ Get details about the client machine and user.
    this info is sent as headers when connecting to the server.
    """
    uname = platform.uname()._asdict() # convert namedtuple to dict
    return {
        "username": getuser(),

        # platform info
        "processor": platform.processor(),
        "system": uname['system'],
        "node": uname['node'],
        "release": uname['release'],
        "version": uname['version'],
        "machine": uname['machine'],
    }