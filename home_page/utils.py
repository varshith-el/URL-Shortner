import string
import random

class Base62Encoder:
    BASE62 = string.ascii_uppercase + string.ascii_lowercase + string.digits

    def encode(self, num, length=6):
        encode = ''
        while num > 0:
            num, remainder = divmod(num, 62)
            encode = self.BASE62[remainder] + encode
        while len(encode) < length:
            encode += random.choice(self.BASE62)
        return encode

    def encode_random(self, length=6):
        random_num = random.randint(0, 62 ** length - 1)
        return self.encode(random_num, length)