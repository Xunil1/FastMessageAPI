if (localStorage.getItem('token') !== null){
    window.location.replace("http://192.168.31.153:8000/");
}

async function authUser(event) {
    event.preventDefault();
    const url = "http://192.168.31.153:8000/user/auth";
    
    const formData = new URLSearchParams();
    formData.append('username', $('#username').val());
    formData.append('password', $('#password').val());

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData.toString()  // данные передаются в формате URLSearchParams
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data["access_token"])
            localStorage.setItem('username', $('#username').val())
            window.location.replace("http://192.168.31.153:8000/");
        } else {
            console.log(response);
            $('#err_box').html(response);
            console.error("Authentication failed:", response.status);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

