import React, {useState} from 'react';
import ReCAPTCHA from 'react-google-recaptcha'

const LoginForm= () => {
    const [email, setEmail]= useState('');
    const [password, setPassword]= useState('');
    const [recaptchaToken, setRecaptchaToken]= useState(null);

    const handleSubmit= (event)=> {
        event.preventDefault();

        if (!recaptchaToken) {
            alert('Please complete the recaptcha!'); // properly handle this response later //
            return;
        }

        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email, password, recaptcha_response: recaptchaToken})
        })
            .then(response => response.json())
            .then(data=> {
                if (data.token) {
                    alert('Login successful!');
                    // handle storing the token and redirecting the user
                } else {
                    alert(data.message);
                }
        })
            .catch(error => {
                console.error('Error',error);
            });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type={email}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder='Email'
                required
            />
            <input
                type={password}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder='Password'
                required
            />
            <ReCAPTCHA
                sitekey='your_google_recaptcha_site_key'
                onChange={(token) => setRecaptchaToken(token)}
            />
            <button type='submit'>Login</button>
        </form>
    );
};

export default LoginForm;