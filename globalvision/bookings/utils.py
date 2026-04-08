import hmac
import hashlib
import base64
import requests
from django.conf import settings


def generate_esewa_signature(total_amount: str, transaction_uuid: str, product_code: str) -> str:
    """
    Generate HMAC-SHA256 Base64 signature for eSewa v2.
    EXACT logic from working sample.
    """
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    secret_key = settings.ESEWA_SECRET_KEY.strip()
    key = secret_key.encode('utf-8')
    
    # Create HMAC-SHA256 signature
    h = hmac.new(key, message.encode('utf-8'), hashlib.sha256)
    signature = base64.b64encode(h.digest()).decode('utf-8')
    
    return signature


def format_amount(amount) -> str:
    """
    Format a Decimal/float/int as a plain string with NO decimal point.
    eSewa v2 sandbox works reliably with whole-number strings ("100", "500").
    For amounts with cents, use two decimal places ("100.50").

    The ONLY requirement is that the exact same string is used in BOTH
    the HMAC message and the HTML form field value — this function
    guarantees that because the view uses the return value for both.
    """
    try:
        f = float(amount)
    except (TypeError, ValueError):
        return "0"

    # Match the 'EventSewa' logic exactly: 
    # Whole numbers get no decimal at all, others get standard string representation
    if f % 1 == 0:
        return str(int(f))
    return str(f)


def verify_esewa_payment(product_code: str, total_amount: str, transaction_uuid: str) -> dict | None:
    """
    Verify a completed eSewa payment by calling eSewa's verification API.
    Returns the parsed JSON on success, or None on failure.

    Docs: https://developer.esewa.com.np/#/epay?id=payment-verification
    """
    import logging
    logger = logging.getLogger(__name__)

    url = settings.ESEWA_VERIFICATION_URL
    params = {
        "product_code": product_code,
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
    }
    
    logger.warning("[eSewa] Verifying: url=%s | params=%s", url, params)

    try:
        # eSewa v2 verification is a GET request with query params
        response = requests.get(url, params=params, timeout=15)
        logger.warning("[eSewa] Verification Response: status=%s | body=%s", response.status_code, response.text)
        
        if response.status_code == 200:
            data = response.json()
            # eSewa returns {"status": "COMPLETE", ...} on success
            if data.get("status") == "COMPLETE":
                return data
    except Exception as e:
        logger.exception("[eSewa] Verification Exception: %s", e)
    
    return None
