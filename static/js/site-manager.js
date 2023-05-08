$(document).ready(function() {
    var apiUrl = $('#sport_name').data('api-url');

    $('#sport_name').select2();
    $('.competitor').select2();

    function updateCompetitorOptions(excludeElement, includeElement, initial = false) {
        var excludeVal = excludeElement.val();
        var options = includeElement.find('option');
        options.each(function() {
            if ($(this).val() == excludeVal) {
                $(this).prop('disabled', true);
            } else {
                $(this).prop('disabled', false);
            }
        });
        includeElement.select2();

        // If it's the initial update, set the value of includeElement to the first non-disabled option
        if (initial) {
            includeElement.val(includeElement.find('option:not([disabled]):first').val()).trigger('change');
        }
    }

    $('#id_side_a').on('change', function() {
        updateCompetitorOptions($(this), $('#id_side_b'));
    });

    $('#id_side_b').on('change', function() {
        updateCompetitorOptions($(this), $('#id_side_a'));
    });

    $('#sport_name').on('change', function() {
        var sport_id = $(this).val();

        $.ajax({
            url: apiUrl,
            data: {
                'sport_id': sport_id
            },
            dataType: 'json',
            success: function(data) {
                var options = '';
                for (var i = 0; i < data.length; i++) {
                    options += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
                }
                $('.competitor').html(options).select2().trigger('change');
                updateCompetitorOptions($('#id_side_a'), $('#id_side_b'), true);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('AJAX error:', textStatus, errorThrown);
            }
        });
    }).trigger('change');


});


document.addEventListener('DOMContentLoaded', () => {
    // Get all update competition buttons
    const updateCompetitionBtns = document.querySelectorAll('.update-competition-btn');
  
    // Add click event listener to each button
    updateCompetitionBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const competitionId = btn.getAttribute('data-competition-id');
        const sideAScore = btn.getAttribute('data-side-a-score');
        const sideBScore = btn.getAttribute('data-side-b-score');
        
        const competitionIdInput = document.getElementById('competitionIdInput');
        const sideAScoreInput = document.getElementById('sideAScoreInput');
        const sideBScoreInput = document.getElementById('sideBScoreInput');
  
        // Set the competition ID input value to the current competition ID
        competitionIdInput.value = competitionId;
        
        // Set the side_a_score and side_b_score input values to the current values
        sideAScoreInput.value = sideAScore;
        sideBScoreInput.value = sideBScore;
  
        // Show the competition update modal
        $('#competitionUpdateModal').modal('show');
      });
    });
  });


// // Get all update competition buttons
// const updateCompetitionBtns = document.querySelectorAll('.update-competition-btn');

// // Add click event listener to each button
// updateCompetitionBtns.forEach(btn => {
//     btn.addEventListener('click', () => {
//     const competitionId = btn.getAttribute('data-competition-id');
//     const competitionIdInput = document.getElementById('competitionIdInput');

//     // Set the competition ID input value to the current competition ID
//     competitionIdInput.value = competitionId;

//     // Show the competition update modal
//     $('#competitionUpdateModal').modal('show');
//     });
// });








