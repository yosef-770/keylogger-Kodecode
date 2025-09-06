
class XorCharCipher:
    """XOR cipher for a single character. Works on UTF-8 encoded bytes and returns hex strings."""

    def __init__(self, key: int):
        """
        Initialize with a single-byte key (0-255).
        Raises ValueError if key is out of range.
        """
        if not isinstance(key, int) or not (0 <= key <= 0xFF):
            raise ValueError("Key must be int in range 0..255")
        self.key = key

    def _to_bytes(self, ch: str) -> bytes:
        """Convert a single character to its UTF-8 bytes representation."""
        if not isinstance(ch, str) or len(ch) == 0:
            raise ValueError("Input must be a non-empty string (single character expected)")
        # allow longer strings but treat whole string bytes (useful in practice)
        return ch.encode('utf-8')

    def encrypt_char(self, ch: str) -> str:
        """
        Encrypt a character (or short string) and return a hex string.
        Example: 'a' -> '03' (example hex)
        """
        b = self._to_bytes(ch)
        xored = bytes([bb ^ self.key for bb in b])
        return xored.hex()

    def decrypt_char(self, hex_str: str) -> str:
        """
        Decrypt a hex string produced by encrypt_char and return the original character/string.
        Raises ValueError for invalid hex or decoding errors.
        """
        try:
            data = bytes.fromhex(hex_str)
        except ValueError:
            raise ValueError("Invalid hex input")

        decoded_bytes = bytes([bb ^ self.key for bb in data])
        try:
            return decoded_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError("Decrypted bytes are not valid UTF-8; possibly wrong key")
