// code specific to the UI in the `/deviations`-route

// Maybe move the slider-init-code from create-slider to here?

$(document).ready(function () {
  // Add initial event hanlder for first deviation taken from template
  $('.remove-deviation').click(removeDeviation)

  $('.period-slider').slider(jQuery.extend(true, {}, options))

  var deviationTemplate = $('.slider-row').clone()

  $('.add-deviation').click(function () {
    var deviation = deviationTemplate.clone()

    // Find and initiate the slider in the new cloned object
    var slider = deviation.find('.period-slider')
    $(slider).slider(jQuery.extend(true, {}, options))

    deviation.find('.remove-deviation').click(removeDeviation)

    $('.buttons').before(deviation)
  })

  function removeDeviation (e) {
    $(e.target).parent().remove()
  }
})
