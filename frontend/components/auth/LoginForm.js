import React, {useState} from "react";
import ReCAPTCHA from 'react-google-recaptcha'

const LoginForm= () => {
    const [email, setEmail]= useState('');
    const [password, setPassword]= useState('');
    const [recaptchaToken, setRecaptchaToken]= useState(null);

    const handleSubmit= (event)=> {
        event.preventDefault();

        if (!recaptchaToken) {
            alert('Please complete recaptcha!'); // properly handle this response later //
        }
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
            }
    }
}