from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import settings


# 加密函数
def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_ECB)  # 使用 ECB 模式加密
    ciphertext = cipher.encrypt(pad(text.encode(), AES.block_size))  # 填充并加密
    # 返回加密后的密文（Base64 编码）
    return base64.b64encode(ciphertext).decode('utf-8')


# 解密函数
def decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)  # 使用 ECB 模式解密
    ciphertext = base64.b64decode(ciphertext)  # 解码 Base64 密文
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')  # 解密并去除填充
    return plaintext


# 主函数
def main():
    key = settings.get_key()  # AES 密钥（16 字节）

    # 明文
    text = "hello"

    # 加密
    encrypted_text = encrypt(text, key)
    print(f"Encrypted Text: {encrypted_text}")

    # 解密
    decrypted_text = decrypt(encrypted_text, key)
    print(f"Decrypted Text: {decrypted_text}")


if __name__ == "__main__":
    main()
