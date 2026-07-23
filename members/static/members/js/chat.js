function sendMessage() {
    var userInput = $('#message').val();
    if (userInput.trim() !== '') {
        $('#chat-messages').append('<p><strong>You:</strong> ' + userInput + '</p>');
        $('#message').val('');

        $.ajax({
            url: CHAT_URL,
            type: 'POST',
            data: {
                'message': userInput
            },
            success: function(response) {
                $('#chat-messages').append('<p><strong>AI:</strong> ' + response.message + '</p>');
            }
        });
    }
}

$('#message').keypress(function(e) {
    if (e.which == 13 && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});