$(document).ready(function () {
    'use strict'
    var first_name = $('#first_name').val()
    var last_name = $('#last_name').val()
    var email = $('#email').val()

    var startDate = $('#start').val()
    var endDate = $('#end').val()

    var savePressed = false



    $('#submit').click(function () {
        savePressed = true
    })

    window.onbeforeunload = function () {

        var preventLeave = false

        if ($('#first_name').val() !== first_name) {
            preventLeave = true
        }

        if ($('#last_name').val() !== last_name) {
            preventLeave = true
        }

        if ($('#email').val() !== email) {
            preventLeave = true
        }

        if ($('#start').val() !== startDate) {
            preventLeave = true
        }

        if ($('#end').val() !== endDate) {
            preventLeave = true
        }

        if (savePressed) {
            preventLeave = false
        }


        if (preventLeave) {
            return 'Du har inte sparat dina ändringar än.'
        }
    }
})