import platform
import uuid
from getpass import getuser


def get_client_details():
    """ Get details about the client machine and user.
    this info is sent as headers when connecting to the server.
    """
    uname = platform.uname()._asdict() # convert namedtuple to dict
    return {
        "username": getuser(), # Machine username
        "display-username": get_display_username(), # <username--@mac_address>, used as identifier in disconnect

        # platform info
        "processor": platform.processor(),
        "system": uname['system'],
        "node": uname['node'],
        "release": uname['release'],
        "version": uname['version'],
        "machine": uname['machine'],
        "mac-address": get_mac_address()
    }

def get_mac_address():
    try:
        mac_int = uuid.getnode()
        # Format the integer into a colon-separated hexadecimal string
        mac_address = ':'.join(['{:02x}'.format((mac_int >> i) & 0xff) for i in range(0, 2 * 6, 2)][::-1])
        return mac_address
    except:
        return 'unknown'

def get_display_username():
    return f'{getuser()}--@{get_mac_address()}'