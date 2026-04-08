import hmac
import hashlib
import base64

def test_signature(total_amount, transaction_uuid, product_code, secret_key):
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    key = secret_key.encode('utf-8')
    h = hmac.new(key, message.encode('utf-8'), hashlib.sha256)
    signature = base64.b64encode(h.digest()).decode('utf-8')
    print(f"Message: {message}")
    print(f"Signature: {signature}")

# Test with standard sandbox values
test_signature("100", "TEST-UUID", "EPAYTEST", "8g8t8h8m6l7m")
