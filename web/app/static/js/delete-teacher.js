$(document).on('click', '.confirm-delete', function () {
    'use strict';
    var firstName = this.dataset.firstname;
    var lastName = this.dataset.lastname;
    var userId = this.dataset.userid;

    bootbox.dialog({
        'message': 'Vill du verkligen ta bort ' + firstName + ' ' + lastName + '?',
        'title': 'Godkänn borttagning',
        'show': true,
        'backdrop': true,
        'closeButton': true,
        'animate': true,
        'buttons': {
            'yes': {
                'label': 'Ja',
                'className': 'btn-success fixed-width-button',
                'callback': function () {
                  var url = $SCRIPT_ROOT + 'admin/teachers/remove'
                  var data = { 'user': userId }

                  $.ajax({type: 'POST', url: url, data: JSON.stringify(data), contentType: 'application/json',
                      success: function () { $('.confirm-delete[data-userId=' + userId + ']').closest('tr').hide() }, error: function () { bootbox.alert('Fel: kunde inte ta bort ' + firstName + " " + lastName) }})
                }
            },
            'no': {
                'label': 'Nej',
                'className': 'btn-danger fixed-width-button'
            }
        }
    });
});