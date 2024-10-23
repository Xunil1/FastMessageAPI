if (sessionStorage.getItem('token') === null){
    window.location.replace("/login");
} else {

    let offset = 0;
    let limit = 50;
    let msg_history = [];
    let allMessagesLoaded = false;

    let prev_scroll_pos = 0;

    let client_id = sessionStorage.getItem('username');
    document.querySelector("#ws-id").textContent = client_id;

    sessionStorage.removeItem("chat_id");
    sessionStorage.removeItem("receiver");
    $('#messageText').prop('disabled', true);
    $('#sbmt_btn').prop('disabled', true);

     $('#messageText').keydown(function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                // Если нажаты Ctrl + Enter
                e.preventDefault(); // Предотвращаем стандартное поведение Enter
                console.log('Отправка сообщения с Ctrl + Enter');
                sendMessage(e);
            } else if (e.key === 'Enter' && !e.shiftKey) {
                // Если только Enter (без Shift)
                e.preventDefault(); // Предотвращаем перенос строки
                console.log('Отправка сообщения с Enter');
                sendMessage(e);
            }
        });

    function scrollToBottom() {
        const chatContainer = document.getElementById('history_view');

        if (chatContainer) {
            // Прокрутка к самому низу контейнера
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }





    let ws = open_connection();

    document.addEventListener("visibilitychange", function() {
        if (document.visibilityState === "visible") {
            if (ws.readyState === 3){
                ws = open_connection();
            }
        }
    });
    
    function open_connection(){
        let src = window.location.host
        let ws = new WebSocket(`ws://${src}/message/ws/${client_id}`);
    
        ws.onopen = function(event) {
            console.log("Connection opened");
            getUsers();
        }


        ws.onmessage = function(event) {
            console.log(event.data);
            const msg = JSON.parse(event.data);

            switch (msg.type) {
                case "error":
                    console.log(msg.detail);
                    break;
                
                case "user_status":
                    let status = $(`#${msg.detail.username}`).find('.user__status')
                    status.text(msg.detail.status);
                    status.removeClass();
                    status.addClass(`user__status ${msg.detail.status}`);
                    if (sessionStorage.getItem("receiver") == msg.detail.username){
                        $("#memberStatus").empty();
                        $('#memberStatus').text(msg.detail.status);
                        $("#memberStatus").removeClass();
                        $("#memberStatus").addClass(msg.detail.status);
                    }
                    break;
                case "message":
                    if (sessionStorage.getItem("receiver") === msg.sender){
                        msg_history.push({
                            "sender": msg.msg.sender,
                            "date": msg.msg.date,
                            "message": msg.msg.message,
                        });
                        render_chat();
                    } else {
                        let status = $(`#${msg.sender}`).find('.messages__count')
                        let msg_count = +status.text();
                        if (msg_count < 1000){
                            msg_count++;
                        } else {
                            msg_count = "999+"
                        }
                        status.text(msg_count);
                    }

                    break;
                case "ok":
                    console.log(msg.detail);
                    msg_history.push({
                        "sender": msg.msg.sender,
                        "date": msg.msg.date,
                        "message": msg.msg.message,
                    });
                    render_chat();
                    break;
            }

        };
        
        ws.onclose = function(event) {
            console.log("Connection closed");
        }
    
        return ws;
    }
    

    $('#history_view').scroll(async function() {
                        if ($(this).scrollTop() === 0 && !allMessagesLoaded) {
                            console.log('Пользователь докрутил до верха!');
                            offset = msg_history.length;
                            prev_scroll_pos = $(this)[0].scrollHeight
                            await get_history(sessionStorage.getItem("chat_id"), msg_history.length, limit);
                            console.log(prev_scroll_pos);
                            console.log($(this)[0].scrollHeight);

                            $(this).scrollTop($(this)[0].scrollHeight - prev_scroll_pos);

                        }
                    });

    async function getUsers(){
        const url = "/user/";

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${sessionStorage.getItem('token')}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                $("#users").empty();
                data["users"].forEach(user => {
                    if (user.username !== sessionStorage.getItem("username"))
                        $("#users").append(
                            `
                                <div class="user" id="${user.username}">
                                    <p><span class="user__name">${user.username}</span></p>
                                    <p><span class="messages__count"></spanclas></p>
                                    <p><span class="user__status ${user.status}">${user.status}</span></p>
                                </div>
                            `
                        )

                })
                $(".user").on( "click", async function() {
                    offset = 0;
                    limit = 50;
                    prev_scroll_pos = 0;
                    await get_chat($(this).attr("id"));
                    let status = $(this).find('.messages__count')
                    status.text("");
                    $("#memberName").empty()
                    $("#memberName").html($(this).attr("id"))
                    $("#memberStatus").empty()
                    $("#memberStatus").html($(this).find('.user__status').text())
                    $("#memberStatus").removeClass();
                    $("#memberStatus").addClass($(this).find('.user__status').text());
                    $('#messageText').prop('disabled', false);
                    $('#sbmt_btn').prop('disabled', false);

                    allMessagesLoaded = false;
                } );
            } else {
                console.error("Failed to retrieve users:", response.status);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }

    async function create_chat(username){
        const url = `/chat/${username}`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${sessionStorage.getItem('token')}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                sessionStorage.setItem("chat_id", data["id"]);
                sessionStorage.setItem("receiver", username);
                await init_messages(data["id"]);
            } else {
                console.error("Failed to retrieve users:", response.status);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }

    async function get_chat(username){
        const url = `/chat/id/${username}`;

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${sessionStorage.getItem('token')}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                sessionStorage.setItem("chat_id", data["id"]);
                sessionStorage.setItem("receiver", username);
                await init_messages(data["id"]);
            } else {
                const errorData = await response.json(); // Попробуем разобрать ответ даже в случае ошибки
                console.error("Failed to retrieve users:", response.status, errorData.detail);
                if (errorData.detail === "Chat not found"){
                    await create_chat(username);
                }
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }
    
    function sendMessage(event) {
        if (ws.readyState === ws.OPEN){
            let rcv = sessionStorage.getItem("username");
            let msg = $('#messageText').val().trim();
            console.log(msg)
            if (msg === '') {
                alert('Сообщение не может быть пустым!');
            } else {
                let send_data = {
                    chat_id: sessionStorage.getItem("chat_id"),
                    username: rcv,
                    message: msg,
                }

                ws.send(JSON.stringify(send_data));

                $('#messageText').val("")

            }

            event.preventDefault()
        } else {
            console.error("Connection closed")
            event.preventDefault()
        }
        
    }
    
    function close_connection(){
        ws.close();
        sessionStorage.clear();
        window.location.replace("/login");
    }

    async function init_messages(chat_id){
        msg_history = [];
        get_history(chat_id, offset, limit);
    }


    async function get_history(chat_id, offset, limit) {
        const url = `/message/${chat_id}?offset=${offset}&limit=${limit}`;
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${sessionStorage.getItem('token')}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                let history = data["history"];
                history.reverse();
                history.forEach(message => {
                    msg_history.push({
                        "sender": message.sender,
                        "date": message.date,
                        "message": message.message,
                    });
                })
                if (history.length === 0){
                    allMessagesLoaded = true;
                }
                await render_chat();
            } else {
                console.error("Failed to retrieve chat:", response.status);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }


    async function render_chat(){
        $("#history_view").empty();
        msg_history.sort((a, b) => Date.parse(a.date) - Date.parse(b.date));
        msg_history.forEach(message => {
            $("#history_view").append(`
                        <div class="message">
                            <div class="message__header">
                                <p><span class="sender">${message.sender}</span></p>
                                <p><span class="date">${message.date}</span></p>
                            </div>
                            <div class="message__content">
                                <pre>${message.message}</pre>
                            </div>
                        </div>`)
        })

        scrollToBottom();
    }

}


