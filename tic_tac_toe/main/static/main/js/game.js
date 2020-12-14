var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/game/' + code_game + '/');

var user = getCookie('user');
var color = getCookie('color');
var turn_div = document.getElementById('turn_message');
var turn = false;
var history_game = [];
var l = false;
chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);

    console.log(data)
    if (data['type'] == 'start'){
        if (data['user'] != user){
            load_div.style.display = 'none';
            your_turn();
        }else if (game_user != user){
            opponent_turn(); 
        }
    }else if (data['type'] == 'turn'){
        history_game.push(parseInt(data['ceil']))
        console.log(history_game)
        if (data['from_user'] == user){
            ceil[parseInt(data['ceil'])].querySelector('#cont').style.background = color;
            if (data['win']){
                l = true;
                turn_div.querySelector("h5").textContent = "Your win";
                show_turn();
                setTimeout("location.href = '/';", 2000)
            } else {
                if (is_draw(data['win'])){
                    turn_div.querySelector("h5").textContent = "Draw";
                    show_turn();
                    setTimeout("location.href = '/';", 2000)
                }else{
                    opponent_turn(); 
                }
            }
        } else {
            ceil[parseInt(data['ceil'])].querySelector('#cont').style.background = invertHex(color);
            turn = true;
            if (is_draw(data['win'])){
                turn_div.querySelector("h5").textContent = "Draw";
                show_turn();
            } else {
                if (data['win']){
                    l = true;
                    turn_div.querySelector("h5").textContent = "Your lose";
                    show_turn();
                } else {
                    your_turn();
                }   
            }
        }
        
    }else if(data['type'] == 'disconnect'){
        if (!l){
            turn_div.querySelector('h5').textContent = "Opponent disconnect";
            show_turn()
            setTimeout("location.href = '/';", 2000)
        }else{
            location.href = '/';
        }
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
    location.href = '/';
};



var my_hod = false;
var battle_ground = document.getElementById('battle');
var ceil = battle_ground.children;
battle_ground.addEventListener('click', function (e){
    var elem = e.target;
    if (elem.parentElement.style.background != ''){
        return
    }
    if (turn){
        if (elem.id == "elem"){
            elem = elem.parentElement.parentElement;
        }
        for (var i in ceil){
            if (ceil[i] == elem){
                var number = i;
            }
        }
        chatSocket.send(JSON.stringify({
            'user': user,
            'ceil': number
        }));
        console.log(number);
        turn = !turn;
    }
})


function invertHex(hex) {
    return "#" + (Number(`0x1${hex.substr(1)}`) ^ 0xFFFFFF).toString(16).substr(1).toUpperCase()
  }
function your_turn(){
    turn_div.querySelector('h5').textContent = "Your Turn";
    show_turn()
}
function opponent_turn(){
    turn_div.querySelector('h5').textContent = "Opponent's Turn";
    show_turn()
}
function show_turn(){
    turn_div.classList.add('show');
    setTimeout("turn_div.classList.remove('show')", 1900);

}

function is_draw(is_win){
    var r = !is_win && history_game.length == 9;
    if (r){l = true}
    return r;
}

if (getCookie('user') == game_user){
    load_div.style.display = 'block';
    turn = !turn;
}
/*
chatSocket.send(JSON.stringify({
    'message': message
}));
*/        

