import { apiToken } from './config.js';
import {coachList} from "./config.js";
import {groupTraining} from "./config.js";

function createGroupTraining(data){
     $.ajax({
        type: 'POST',
        url: groupTraining,
        headers: {
            'Authorization': apiToken,
            'X-CSRFToken': get_csrf(),
            'Content-Type': 'application/json'
        },
        data: JSON.stringify(data),

        success: function (response) {
            $('#coach-modal').hide();
            $('#link-modal').show();
        },
     });
}

function get_csrf(){
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

$(document).ready(function() {
    const url  = window.location.pathname
    const groupId = url.split('/')[2];
    $(window).click(function(event) {
      if (event.target == document.getElementById('coach-modal')) {
        $('#coach-modal').hide();
      }
    });

    $(window).click(function(event) {
      if (event.target == document.getElementById('link-modal')) {
        $('#link-modal').hide();
      }
    });
    $('#start-class-btn').on('click', function () {

        $.get({
              url: `${coachList}${groupId}/`,
              headers: {
                'Authorization': apiToken,
              },
              success: function (data) {
                  let body = {
                    'coach': null,
                    'group': Number(groupId)
                  }
                  if (data.base_coach === null & data.other_coaches.length === 0) {
                      createGroupTraining(body)
                  } else {
                      let coachList = '<ul>';
                      if (data.base_coach != null) {
                          let coachLastName = ''
                            if (data.base_coach.last_name) {
                                coachLastName = data.base_coach.last_name
                            }
                            coachList += '<li><input type="radio" name="coach" value="' + data.base_coach.id + '">' + ' ' + data.base_coach.first_name + ' ' + coachLastName + '</li>';
                      }
                      if (data.other_coaches != null) {
                          $.each(data.other_coaches, function (index, coach) {
                            let coachLastName = ''
                            if (coach.last_name) {
                                coachLastName = coach.last_name
                            }
                            coachList +=
                                '<li><input type="radio" name="coach" value="' + coach.id + '">' + ' ' + coach.first_name + ' ' + coachLastName + '</li>';
                            });
                      }
                      coachList += '</ul>';
                    $('#coach-list').html(coachList);
                    $('#coach-modal').show();
                  }
              }
        });
    });

    $('#accept-coach-btn').on('click', function () {
        let coachId = $('input[name="coach"]:checked').val();
        let data = {
            'coach': Number(coachId),
            'group': Number(groupId)
        }
        createGroupTraining(data)
    });
})