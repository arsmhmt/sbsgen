LANGUAGES = {
    'en': {
        'verify_subject': 'Verify your SmartSlip account',
        'verify_body': 'Welcome to SmartSlip! Please verify your email by clicking the link below:',
        'already_verified': 'Email already verified.',
        'verification_success': 'Email verified!',
        'verification_failed': 'Verification failed.',
        'email_sent': 'Verification email sent.',
        'email_error': 'Error sending email.'
    },
    'tr': {
        'verify_subject': 'SmartSlip hesabınızı doğrulayın',
        'verify_body': 'SmartSlip’e hoş geldiniz! Lütfen aşağıdaki bağlantıya tıklayarak e-postanızı doğrulayın:',
        'already_verified': 'E-posta zaten doğrulandı.',
        'verification_success': 'E-posta doğrulandı!',
        'verification_failed': 'Doğrulama başarısız oldu.',
        'email_sent': 'Doğrulama e-postası gönderildi.',
        'email_error': 'E-posta gönderilirken hata oluştu.'
    }
}

def get_text(key, lang='en'):
    return LANGUAGES.get(lang, LANGUAGES['en']).get(key, key)
