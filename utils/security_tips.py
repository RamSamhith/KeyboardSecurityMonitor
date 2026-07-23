"""
Security Tips Module
Provides educational cybersecurity tips
"""

# List of security tips for educational purposes
SECURITY_TIPS = [
    {
        "title": "Input Validation",
        "tip": "Always validate user input on both client and server side to prevent injection attacks."
    },
    {
        "title": "Password Security",
        "tip": "Use strong, unique passwords with a mix of characters. Never reuse passwords across sites."
    },
    {
        "title": "Two-Factor Authentication",
        "tip": "Enable 2FA wherever possible to add an extra layer of security to your accounts."
    },
    {
        "title": "Software Updates",
        "tip": "Keep your software updated to patch known vulnerabilities and security flaws."
    },
    {
        "title": "Phishing Awareness",
        "tip": "Be cautious of unsolicited emails asking for personal information. Verify sender authenticity."
    },
    {
        "title": "Data Encryption",
        "tip": "Encrypt sensitive data both at rest and in transit to protect it from unauthorized access."
    },
    {
        "title": "Secure Coding",
        "tip": "Follow secure coding practices to prevent common vulnerabilities like XSS and SQL injection."
    },
    {
        "title": "Network Security",
        "tip": "Use secure networks and avoid public Wi-Fi for sensitive transactions without VPN."
    },
    {
        "title": "Access Control",
        "tip": "Implement principle of least privilege - only grant necessary access permissions."
    },
    {
        "title": "Security Logging",
        "tip": "Maintain comprehensive logs to detect and investigate security incidents."
    }
]

def get_random_tip():
    """Get a random security tip"""
    import random
    return random.choice(SECURITY_TIPS)

def get_all_tips():
    """Get all security tips"""
    return SECURITY_TIPS
