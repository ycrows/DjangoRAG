function sendMessage() {
    var userInput = $('#message').val();
    const message = document.getElementById("message").value;

    if (userInput.trim() !== '') {
        $('#chat-messages').append('<p><strong>You:</strong> ' + userInput + '</p>');
        $('#message').val('');

        $.ajax({
            url: CHAT_URL,
            type: 'POST',
            data: {
                'message': userInput,
                'preset': selectedPreset
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

let selectedPreset = '';
document.querySelectorAll(".dropdown-item").forEach(item => {
    item.addEventListener("click", function () {
        const presetName = this.textContent.trim();
        const presetSlug = this.dataset.preset;
        
        // Update the visible button
        document.getElementById("preset-dropdown-btn").textContent = presetName;

        // Save the selected preset
        selectedPreset = presetSlug;

        console.log("Selected preset:", selectedPreset);
    });
});