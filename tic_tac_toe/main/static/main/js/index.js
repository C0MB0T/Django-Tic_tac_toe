var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/lobby/');

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = JSON.parse( data['message'] );
    if (message['type'] == 'add'){
        var elem = document.createElement('div');
        elem.innerHTML = '<a href="/join/' + message['code'] + '">' + message['user'] + '</a>';
        document.getElementById('rooms').append(elem);
    } else {
        document.querySelector('a[href="/join/' + message['code'] + '"]').remove()
    }
    console.log(message)
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

var inp = document.getElementById('nick');
inp.addEventListener('keyup', function(e){
    document.cookie = "user=" + inp.value + ";path=/";
})
var color = document.getElementById('color');
color.addEventListener('change', function(e){
    document.cookie = "color=" + color.value + ";path=/";
})

color.value = getCookie('color');
inp.value = getCookie('user');
/*
chatSocket.send(JSON.stringify({
    'message': message
}));
*/        

