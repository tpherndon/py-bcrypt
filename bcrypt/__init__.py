"""OpenBSD Blowfish password hashing.

This module implements the OpenBSD Blowfish password hashing
algorithm, as described in "A Future-Adaptable Password Scheme" by
Niels Provos and David Mazieres.

This system hashes passwords using a version of Bruce Schneier's
Blowfish block cipher with modifications designed to raise the cost
of off-line password cracking. The computation cost of the algorithm
is parametised, so it can be increased as computers get faster.

Passwords are hashed using the hashpw() routine:

  hashpw(password, salt) -> hashed_password

Salts for the the second parameter may be randomly generated using the
gensalt() function:

  gensalt(log_rounds = 12) -> random_salt

The parameter "log_rounds" defines the complexity of the hashing. The
cost increases as 2**log_rounds.

Passwords and salts for the hashpw and gensalt functions are text strings
that must not contain embedded nul (ASCII 0) characters.

This module also operates as a key derivation function (KDF) to transform a
password and salt into bytes suitable for use as cryptographic key material:

  kdf(password, salt, desired_length, rounds) -> key

This will generate a key of "desired_length" in bytes (NB. not bits). For the
KDF mode the "rounds" parameter is the literal rounds, not the logarithm as
for gensalt. For the KDF case, "salt" and "password" may be binary strings
containing embedded nul characters.

The KDF mode is recommended for generating symmetric cipher keys, IVs, hash
and MAC keys, etc. It should not be used a keystream for encryption itself.
"""

import os
from bcrypt._bcrypt import *

def gensalt(log_rounds = 12):
	"""Generate a random text salt for use with hashpw(). "log_rounds"
	defines the complexity of the hashing, increasing the cost as
	2**log_rounds."""
	return encode_salt(os.urandom(16), min(max(log_rounds, 4), 31))

