//$(document).ready(function() {
//    alert('Hello, world!');
//});


$(document).ready(function() {

    $("#about-btn").removeClass('btn-primary').addClass('btn-success').click(function() {
        alert('You clicked the button using JQuery!');
    });

    $('.ouch').click(function() {
        alert('You clicked me! Ouch!');
    });

    $('#about-btn').click(function() {
        msgStr = $('#msg').html();
        msgStr = msgStr + ' ooo, fancy!';

        $('#msg').html(msgStr);
    });

});



$('p').hover(
    function() {
        $(this).css('color', 'red');
    },
    function() {
        $(this).css('color', 'black');
});
