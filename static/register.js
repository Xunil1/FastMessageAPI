if (sessionStorage.getItem('token') !== null){
    window.location.replace("/");
}

async function registerUser(event) {
    event.preventDefault();
    const url = "/user/";

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "username": $('#username').val(),
                "password": $('#password').val(),
            }),
        });

        if (response.ok) {
            const data = await response.json();
            sessionStorage.setItem('username', data["username"]);
            window.location.replace("/login");
        } else {
            console.log(response);
            $('#err_box').html(response);
            console.error("Authentication failed:", response.status);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

