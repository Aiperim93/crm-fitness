import {lazyDays} from "./config.js";

function get_csrf() {
    let cookie = document.cookie.split(';');
    let token = ''
    for (let i = 0; i < cookie.length; i++) {
        let b = cookie[i].split('=')
        b[0] = b[0].replace(/\s+/g, '')
        if (b[0] === 'csrftoken') {
          token = b[1]
        }
    }
    return token
}

function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}


$(document).ready(function() {
    const freezeIcon = $('.freeze-btn');

    $(window).click(function(event) {
        if (event.target == document.getElementById('freeze-modal')) {
            $('#freeze-modal').hide();
        }
    });

    freezeIcon.on('click', function () {
        $('#error').text("");
        $('#freeze-modal').show();
        const clientId = $(this).data('client-id');

        $('#freeze-button').on('click', function (){
            const today = formatDate(new Date());
            const startDate = $("#start-date").val();
            const endDate = $("#end-date").val();
            if (startDate < today) {
                $('#error').text("Дата начала не может быть раньше текущей даты");
            } else if (endDate < startDate) {
                $('#error').text("Дата окончания не может быть раньше даты начала");
            } else if (endDate === startDate) {
                $('#error').text("Дата окончания не может быть равна дате начала");
            }else {
                const url = `${lazyDays}${clientId}/`;
                const data = {start_date: startDate, end_date: endDate};

                $.ajax({
                    url: url,
                    type: "POST",
                    headers: {
                        'X-CSRFToken': get_csrf(),
                        'Content-Type': 'application/json'
                    },
                    data: JSON.stringify(data),
                    processData: false,
                    success: function(data) {
                        showMessage("Заморозка добавлена успешно!", "success");
                        $('#error').text("");
                        $('#freeze-modal').hide();
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        if (errorThrown !== 'Bad Request') {
                             showMessage("Что-то пошло не так. Пожалуйста, повторите попытку позже.", "error");
                        }
                    }
                });
            }


            function showMessage(message, type) {
                const messageElement = $('<div>').addClass(type).text(message);
                $('#message').html(messageElement);

                setTimeout(function() {
                    messageElement.remove();
                }, 3000);
            }
        });
    });
});