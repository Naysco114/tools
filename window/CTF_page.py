import base64
import hashlib
import socket
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
)
from urllib.parse import quote, unquote


class CTFPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CTF工具箱")
        layout = QVBoxLayout()

        # 编码解码部分
        encode_decode_layout = QVBoxLayout()
        encode_decode_label = QLabel("编码解码")
        encode_decode_layout.addWidget(encode_decode_label)

        self.encode_decode_text_input = QLineEdit()
        encode_decode_layout.addWidget(self.encode_decode_text_input)

        encode_button = QPushButton("编码")
        encode_button.clicked.connect(self.encode_text)
        encode_decode_layout.addWidget(encode_button)

        decode_button = QPushButton("解码")
        decode_button.clicked.connect(self.decode_text)
        encode_decode_layout.addWidget(decode_button)

        layout.addLayout(encode_decode_layout)

        # 密码学工具部分
        cryptography_layout = QVBoxLayout()
        cryptography_label = QLabel("密码学工具")
        cryptography_layout.addWidget(cryptography_label)

        self.hash_text_input = QLineEdit()
        cryptography_layout.addWidget(self.hash_text_input)

        hash_button = QPushButton("哈希")
        hash_button.clicked.connect(self.hash_text)
        cryptography_layout.addWidget(hash_button)

        layout.addLayout(cryptography_layout)

        # 网络扫描器部分
        network_scanner_layout = QVBoxLayout()
        network_scanner_label = QLabel("网络扫描器")
        network_scanner_layout.addWidget(network_scanner_label)

        self.host_input = QLineEdit()
        network_scanner_layout.addWidget(self.host_input)

        self.ports_input = QLineEdit()
        network_scanner_layout.addWidget(self.ports_input)

        scan_button = QPushButton("扫描")
        scan_button.clicked.connect(self.scan_ports)
        network_scanner_layout.addWidget(scan_button)

        layout.addLayout(network_scanner_layout)

        # 其他功能部分
        other_layout = QVBoxLayout()
        other_label = QLabel("其他功能")
        other_layout.addWidget(other_label)

        rsa_encrypt_button = QPushButton("RSA加密")
        rsa_encrypt_button.clicked.connect(self.rsa_encrypt_text)
        other_layout.addWidget(rsa_encrypt_button)

        rsa_decrypt_button = QPushButton("RSA解密")
        rsa_decrypt_button.clicked.connect(self.rsa_decrypt_text)
        other_layout.addWidget(rsa_decrypt_button)

        base32_encode_button = QPushButton("Base32编码")
        base32_encode_button.clicked.connect(self.base32_encode_text)
        other_layout.addWidget(base32_encode_button)

        base32_decode_button = QPushButton("Base32解码")
        base32_decode_button.clicked.connect(self.base32_decode_text)
        other_layout.addWidget(base32_decode_button)

        url_encode_button = QPushButton("URL编码")
        url_encode_button.clicked.connect(self.url_encode_text)
        other_layout.addWidget(url_encode_button)

        url_decode_button = QPushButton("URL解码")
        url_decode_button.clicked.connect(self.url_decode_text)
        other_layout.addWidget(url_decode_button)

        rot13_encrypt_button = QPushButton("ROT13加密")
        rot13_encrypt_button.clicked.connect(self.rot13_encrypt_text)
        other_layout.addWidget(rot13_encrypt_button)

        rot13_decrypt_button = QPushButton("ROT13解密")
        rot13_decrypt_button.clicked.connect(self.rot13_decrypt_text)
        other_layout.addWidget(rot13_decrypt_button)

        layout.addLayout(other_layout)

        # 输出结果
        self.output_text = QTextEdit()
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def encode_text(self):
        text = self.encode_decode_text_input.text()
        encoded_text = base64.b64encode(text.encode()).decode()
        self.output_text.setPlainText(encoded_text)

    def decode_text(self):
        encoded_text = self.encode_decode_text_input.text()
        decoded_text = base64.b64decode(encoded_text.encode()).decode()
        self.output_text.setPlainText(decoded_text)

    def hash_text(self):
        text = self.hash_text_input.text()
        hash_result = hashlib.sha256(text.encode()).hexdigest()
        self.output_text.setPlainText(hash_result)

    def scan_ports(self):
        host = self.host_input.text()
        ports = self.ports_input.text().split(",")
        ports = [int(port.strip()) for port in ports]
        results = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, port))
            if result == 0:
                results.append(f"Port {port}: Open")
            else:
                results.append(f"Port {port}: Closed")
            sock.close()
        self.output_text.setPlainText("\n".join(results))

    def rsa_encrypt_text(self):
        # Add your RSA encryption logic here
        pass

    def rsa_decrypt_text(self):
        # Add your RSA decryption logic here
        pass

    def base32_encode_text(self):
        text = self.encode_decode_text_input.text()
        encoded_text = self.base32_encode(text)
        self.output_text.setPlainText(encoded_text)

    def base32_decode_text(self):
        encoded_text = self.encode_decode_text_input.text()
        decoded_text = self.base32_decode(encoded_text)
        self.output_text.setPlainText(decoded_text)

    def url_encode_text(self):
        text = self.encode_decode_text_input.text()
        encoded_text = quote(text)
        self.output_text.setPlainText(encoded_text)

    def url_decode_text(self):
        encoded_text = self.encode_decode_text_input.text()
        decoded_text = unquote(encoded_text)
        self.output_text.setPlainText(decoded_text)

    def rot13_encrypt_text(self):
        text = self.encode_decode_text_input.text()
        encrypted_text = ''.join([chr((ord(c) - 65 + 13) % 26 + 65) if c.isupper() else chr(
            (ord(c) - 97 + 13) % 26 + 97) if c.islower() else c for c in text])
        self.output_text.setPlainText(encrypted_text)

    def rot13_decrypt_text(self):
        text = self.encode_decode_text_input.text()
        decrypted_text = ''.join([chr((ord(c) - 65 - 13) % 26 + 65) if c.isupper() else chr(
            (ord(c) - 97 - 13) % 26 + 97) if c.islower() else c for c in text])
        self.output_text.setPlainText(decrypted_text)

    def base32_encode(self, text):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
        result = ''
        padding = ''
        if len(text) % 5 != 0:
            padding = '=' * (8 - (len(text) * 8 % 5) // 5)
            text += '\x00' * ((5 - len(text) * 8 % 5) // 8)
        for i in range(len(text) // 5):
            val = int.from_bytes(text[i * 5: i * 5 + 5], 'big')
            for j in range(8):
                result += alphabet[val & 31]
                val >>= 5
        return result + padding

    def base32_decode(self, text):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
        result = bytearray()
        padding = text[-6:]
        for i in range(len(text) // 8):
            val = 0
            for j in range(8):
                val <<= 5
                val += alphabet.index(text[i * 8 + 7 - j])
            result.extend(val.to_bytes(5, 'big'))
        return bytes(result.rstrip(b'\x00')).decode()
