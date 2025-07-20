// static/js/social-auth.js
// Handles social login button redirects (stub for now)
document.getElementById('googleLogin')?.addEventListener('click', function() {
  window.location.href = '/auth/google';
});
document.getElementById('facebookLogin')?.addEventListener('click', function() {
  window.location.href = '/auth/facebook';
});
document.getElementById('appleLogin')?.addEventListener('click', function() {
  window.location.href = '/auth/apple';
});
document.getElementById('googleSignup')?.addEventListener('click', function() {
  window.location.href = '/auth/google';
});
document.getElementById('facebookSignup')?.addEventListener('click', function() {
  window.location.href = '/auth/facebook';
});
document.getElementById('appleSignup')?.addEventListener('click', function() {
  window.location.href = '/auth/apple';
});
