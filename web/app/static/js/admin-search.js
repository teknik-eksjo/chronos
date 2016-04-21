function contains(str, substr) {
  /*
  Return true if str contains substr
  */
  return str.indexOf(substr) > -1
}

function filterTeachers(query) {
  /*
  Search for teachers with a specific name and only show relevant results
  */
  var teachers = $('.teacher')
  query = query.toLowerCase()

  teachers.each(function() {
    var firstName = this.children[0].innerText.toLowerCase()
    var lastName = this.children[1].innerText.toLowerCase()
    var email = this.children[2].innerText.toLowerCase()

    // Only show relevant teachers in UI
    if (contains(firstName, query) || contains(lastName, query) || contains(email, query)) {
      $(this).show()
    } else {
      $(this).hide()
    }
  })
}

$(document).ready(function() {
  var search = $('#search')
  search.focus()

  search.on('input', function(e) {
    filterTeachers(search.val())
  })

  search.on('keydown', function(e) {
    if (e.keyCode === 13) {
      filterTeachers(search.val())
      search.val('')
    }
  })
})
