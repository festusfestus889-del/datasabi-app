import requests
import streamlit.components.v1 as components


# Paystack Keys - safe version that won't crash
try:
    PAYSTACK_SECRET = st.secrets["PAYSTACK_SECRET_KEY"]
    PAYSTACK_PUBLIC = st.secrets["PAYSTACK_PUBLIC_KEY"]
except:
    PAYSTACK_SECRET = "sk_test_733f7ed426305d8ade9d396ca721d21d0b040fc7"
    PAYSTACK_PUBLIC = "pk_test_779701e221cab35814d81817c5a86bbd3b23e153"
def verify_paystack_payment(reference):
    """Verifies if Paystack payment is successful"""
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET}"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        if data["status"] and data["data"]["status"] == "success":
            return True, data["data"]
        return False, data
    except Exception as e:
        return False, str(e)

def paystack_button(email, amount_kobo=200000): # 200000 kobo = N2,000
    """Generates Paystack Inline button that auto-verifies"""
    # Generate unique ref
    ref = f"DATASABI_{int(datetime.now().timestamp())}"
    
    btn_code = f"""
    <script src="https://js.paystack.co/v1/inline.js"></script>
    <button id="pay-btn" style="
        background:#0AA06E; color:white; padding:14px 28px; 
        border:none; border-radius:8px; font-size:16px; 
        font-weight:bold; width:100%; cursor:pointer;">
        💳 Pay ₦2,000 with Paystack - Unlock Report
    </button>
    <script>
    document.getElementById('pay-btn').onclick = function(){{
        var handler = PaystackPop.setup({{
            key: '{PAYSTACK_PUBLIC}',
            email: '{email}',
            amount: {amount_kobo},
            currency: 'NGN',
            ref: '{ref}',
            callback: function(response){{
                window.parent.postMessage({{type:'PAYSTACK_SUCCESS', reference: response.reference}}, '*');
            }},
            onClose: function(){{
                alert('Payment window closed. Click pay again to continue.');
            }}
        }});
        handler.openIframe();
    }}
    </script>
    """
    components.html(btn_code, height=80)
    return ref
