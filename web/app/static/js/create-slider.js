$(function () {
  // create slider with an options object that will override the defaut config.
  var options = {
    min: 360,
    max: 1080,
    step: 5,
    tooltips: true,
    handles: [{
      value: 480,
      type: 'wake'
    }, {
      value: 690,
      type: 'leave'
    }, {
      value: 750,
      type: 'return'
    }, {
      value: 960,
      type: 'sleep'
    }],
    showTypeNames: true,
    typeNames: {
      'wake': 'Start',
      'leave': 'Lunch',
      'return': 'Lunch slut',
      'sleep': 'Slut'
    },
    mainClass: 'sleep',   // Main css class (default background style of slider)
    type: 'time',
    slide: function (e, ui) {
      // Work persiods no longer than 5h
      if (ui.values[1] - ui.values[0] > 300) {
        $(jQuery(this).children('.ui-slider-range.wake')).addClass('errorbg')
      } else {
        $(jQuery(this).children('.ui-slider-range.wake')).removeClass('errorbg')
      }

      // Lunch break must be at least 30 minutes
      if (ui.values[2] - ui.values[1] < 30) {
        $(jQuery(this).children('.ui-slider-range.leave')).addClass('errorbg')
      } else {
        $(jQuery(this).children('.ui-slider-range.leave')).removeClass('errorbg')
      }

      // Work period 2 can't be longer than 5 hours
      if (ui.values[3] - ui.values[2] > 300) {
        $(jQuery(this).children('.ui-slider-range.return')).addClass('errorbg')
      } else {
        $(jQuery(this).children('.ui-slider-range.return')).removeClass('errorbg')
      }
    },
    change: function (e, ui) {
      //TODO: send updated info to server here.
    }
  }

  $('.period-slider').slider(options)
})
