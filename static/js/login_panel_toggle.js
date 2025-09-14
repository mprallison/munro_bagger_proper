// toggle login form
const toggleLink = document.getElementById('toggle-form');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const formTitle = document.getElementById('form-title');

toggleLink.addEventListener('click', function(e) {
  e.preventDefault();

  if (signupForm.style.display === 'none') {
    // Show signup, hide login
    loginForm.style.display = 'none';
    signupForm.style.display = 'block';
    formTitle.textContent = 'Sign Up';
    toggleLink.textContent = 'To login';
  } else {
    // Show login, hide signup
    signupForm.style.display = 'none';
    loginForm.style.display = 'block';
    formTitle.textContent = 'Login';
    toggleLink.textContent = 'To sign up';
  }
});