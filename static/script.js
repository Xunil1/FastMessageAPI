if (localStorage.getItem('token') === null){
    window.location.replace("http://192.168.31.153:8000/login");
} else {
    let client_id = localStorage.getItem('username');
    document.querySelector("#ws-id").textContent = client_id;
    
    
    
    function open_connection(){
        let ws = new WebSocket(`ws://192.168.31.153:8000/message/ws/${client_id}`);
    
        ws.onopen = function(event) {
            console.log("Connection opened");
            getChat();
        }
        
        ws.onmessage = function(event) {
            console.log(event.data);
            const msg = JSON.parse(event.data);
            console.log(msg.type);

            switch (msg.type) {
                case "error":
                    console.log(msg.detail);
                    break;
                
                case "user_status":
                    if (localStorage.getItem("receiver") == msg.detail.username){
                        $('#memberStatus').empty();
                        $('#memberStatus').html(msg.detail.status);
                    }
                    break;
                default:
                    get_history(localStorage.getItem("chat_id"));
                    break;
            }

            
            // let messages = document.getElementById('messages')
            // let message = document.createElement('li')
            // let content = document.createTextNode(event.data)
            // message.appendChild(content)
            // messages.appendChild(message)
        };
        
        ws.onclose = function(event) {
            console.log("Connection closed");
        }
    
        return ws;
    }
    
    let ws = open_connection();
    
    
    
    function sendMessage(event) {
        if (ws.readyState === ws.OPEN){
            let rcv = localStorage.getItem("username")
            let msg = $('#messageText').val();

            let send_data = {
                chat_id: localStorage.getItem("chat_id"),
                username: rcv,
                message: msg,
            }

            ws.send(JSON.stringify(send_data));


            $('#messageText').val("")
            event.preventDefault()
        } else {
            console.error("Connection closed")
            event.preventDefault()
        }
        
    }
    
    function close_connection(){
        ws.close();
        console.log(ws);
    }

    async function getChat() {
        const url = "http://192.168.31.153:8000/chat/";
    
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
    
            if (response.ok) {
                const data = await response.json();
                $("#chatSelect").empty();
                $("#chatSelect").append(`<option disabled selected>--Выберите чат--</option>`);
                data["chats"].forEach(element => {
                    $("#chatSelect").append(`<option value="${element}">${element}</option>`);
                });
                
                console.log(data["chats"]);
            } else {
                console.error("Failed to retrieve chat:", response.status);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }

    $("select").change(function(){
        localStorage.setItem("chat_id", $(this).val())
        getChatInfo($(this).val());
    });
}

async function getChatInfo(chat_id) {
    const url = `http://192.168.31.153:8000/chat/${chat_id}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            data["members"].forEach(member => {
                if (member["username"] != localStorage.getItem("username")){
                    $('#memberName').empty();
                    $('#memberName').html(member["username"])
                    localStorage.setItem("receiver", member["username"])
                    $('#memberStatus').empty();
                    $('#memberStatus').html(member["status"]);
                }
            })
            get_history(chat_id);
            
        } else {
            console.error("Failed to retrieve chat:", response.status);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

async function get_history(chat_id) {
    const url = `http://192.168.31.153:8000/message/${chat_id}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            $("#history").empty();
            data["history"].forEach(message => {
                $("#history").append(`
                    <div class="message">
                        <div class="message__header">
                            <span class="sender_name" style="font-weight: bold;">${message["sender"]}</span> <span class="sender_date">${message["date"]}</span>
                        </div>
                        <div class="content" style="margin-left: 10px;">
                            ${message["message"]}
                        </div>
                    </div>`)
            })
            
            
        } else {
            console.error("Failed to retrieve chat:", response.status);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}
