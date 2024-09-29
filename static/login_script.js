async function displayLoginForm (login, password, enterTxt) {
    let pageContainer = document.querySelector('.my-page-container')
    let formContainer = document.querySelector('.login-form-container')

    const form = document.createElement('form');
    form.setAttribute('id', 'loginForm');
    form.setAttribute('action', '/api/authorization');
    form.setAttribute('type', 'POST')

    const loginInput = document.createElement('input');
    loginInput.setAttribute('type', 'text');
    loginInput.setAttribute('id', 'formLogin');
    loginInput.setAttribute('name', 'login');
    loginInput.setAttribute('required', 'true');
    loginInput.setAttribute('placeholder', login);
    loginInput.classList.add('login-input')

    const passwordInput = document.createElement('input');
    passwordInput.setAttribute('type', 'password');
    passwordInput.setAttribute('id', 'formPassword');
    passwordInput.setAttribute('name', 'password');
    passwordInput.setAttribute('required', 'true');
    passwordInput.setAttribute('placeholder', password);
    passwordInput.classList.add('password-input')

    const submitButton = document.createElement('button');
    submitButton.setAttribute('type', 'submit');
    submitButton.innerText = enterTxt
    submitButton.classList.add('next-btn')
    submitButton.classList.add('login-btn')

    let loginErrSpan = document.createElement('span')
    loginErrSpan.classList.add('login-error-txt')
    let passErrorSpan = document.createElement('span')
    passErrorSpan.classList.add('login-error-txt')

    let loginSpinner = document.createElement('span')
    loginSpinner.classList.add('login-spinner')

    form.appendChild(loginInput)
    form.appendChild(loginErrSpan)
    form.appendChild(passwordInput)
    form.appendChild(passErrorSpan)
    form.appendChild(submitButton)
    formContainer.appendChild(form)
    pageContainer.appendChild(loginSpinner)

    function cleanErrorMessages () {
        loginErrSpan.innerText = ''
        passErrorSpan.innerText = ''
    }

    form.addEventListener('submit',async function (event) {
        event.preventDefault();
        cleanErrorMessages()
        const formData = new FormData(form);
        loginSpinner.style.display = 'block';
        submitButton.disabled = true;
        try {
            let response = await fetch('/api/authorization', {
                method: 'POST',
                body: formData
            })
            let resp_data = await response.json()
            if (resp_data.resp_status === 'ok') {
                window.location.href = '/'
            } else if (resp_data.resp_status === 'login_error') {
                loginErrSpan.innerText = resp_data.err_msg;
                // } else if (resp_data.resp_status === 'password_error') {
                //     passErrorSpan.innerText = data.err_msg
            }
        } catch (err) {
            console.error(err)
        } finally {
            loginSpinner.style.display = 'none';
            submitButton.disabled = false;
        }
    });
}
