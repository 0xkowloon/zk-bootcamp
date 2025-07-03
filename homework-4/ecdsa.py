import hashlib
import hmac
import secrets
from ecpy.curves import Curve

class Signer:
    def __init__(self, curve):
        self.curve = curve
        self.pkey = self.generate_pkey()
        self.pubkey = self.get_pubkey(self.pkey)

    def generate_pkey(self):
        return secrets.randbelow(self.curve.order - 1) + 1

    def get_pubkey(self, pkey):
        return self.curve.generator * pkey

class ECDSA:
    def __init__(self, curve):
        self.curve = curve
        self.G = self.curve.generator
        self.order = self.curve.order

    def hash(self, message):
        """
        Hash the message and truncate to the bit length of the curve order, as per ECDSA standard.
        """
        hash_bytes = hashlib.sha256(message.encode()).digest()
        hash_int = int.from_bytes(hash_bytes, 'big')
        order_bits = self.order.bit_length()
        hash_bits = len(hash_bytes) * 8
        if hash_bits > order_bits:
            # Truncate to the leftmost order_bits
            hash_int = hash_int >> (hash_bits - order_bits)
        return hash_int

    def assert_range(self, value):
        assert 1 <= value <= self.order - 1, "value is not in the range [1, n-1]"

    def mul_inv(self, val):
        return pow(val, self.order - 2, self.order)

    def generate_k(self):
        return secrets.randbelow(self.order - 1) + 1

    def int2octets(self, val):
        return val.to_bytes(32, 'big')

    def bits2int(self, val):
        return int.from_bytes(val, 'big')

    def hmac(self, K, V):
        return hmac.new(K, V, hashlib.sha256).digest()

    def generate_k_deterministic(self, h1, x):
        """
        Deterministically generate the nonce k for ECDSA signing using HMAC, as specified in RFC 6979.

        Args:
            h1 (int): The hash of the message to be signed, as an integer. This is typically the output of the hash function applied to the message.
            x (int): The signer's private key, as an integer.

        Returns:
            int: A deterministic nonce k in the range [1, order-1].
        """
        x_bytes = self.int2octets(x)
        h1_bytes = self.int2octets(h1)

        V = b'\x01' * 32
        K = b'\x00' * 32

        K = self.hmac(K, V + b'\x00' + x_bytes + h1_bytes)
        V = self.hmac(K, V)
        K = self.hmac(K, V + b'\x01' + x_bytes + h1_bytes)
        V = self.hmac(K, V)

        while True:
            V = self.hmac(K, V)
            k = self.bits2int(V)

            if 1 <= k and k <= self.order - 1:
                return k

            K = self.hmac(K, V + b'\x00')
            V = self.hmac(K, V)

    def sign(self, message, pkey):
        h = self.hash(message)
        # k = self.generate_k()
        k = self.generate_k_deterministic(h, pkey)
        R = self.G * k
        r = R.x
        s = self.mul_inv(k) * (h + r * pkey) % self.order
        self.assert_range(r)
        self.assert_range(s)
        return r, s

    def verify(self, message, r, s, pubkey):
        h = self.hash(message)
        s1 = self.mul_inv(s)
        u1 = (h * s1) % self.order
        u2 = (r * s1) % self.order
        R_prime = u1 * self.G + u2 * pubkey
        r_prime = R_prime.x % self.order
        assert r == r_prime, "Signature verification failed"

if __name__ == "__main__":
    curve = Curve.get_curve('secp256k1')
    signer = Signer(curve)
    ecdsa = ECDSA(curve)
    message = "Send 10,000 BTC to 0xkowloon"
    r, s = ecdsa.sign(message, signer.pkey)
    ecdsa.verify(message, r, s, signer.pubkey)