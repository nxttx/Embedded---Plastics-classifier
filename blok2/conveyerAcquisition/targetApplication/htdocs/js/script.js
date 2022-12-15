document.addEventListener('DOMContentLoaded', function() {

  /** 
   * toggle sidenav
   */ 
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems);


  /**
   * set all checkboxes
   */
  var elems = document.querySelectorAll('.checkbox');
  elems.forEach(function(elem) {
    // get data-id
    var id = elem.getAttribute('data-id');
    // check in local storage what the value was
    if (localStorage.getItem("SETTING_"+id) == null) {
      // if there is no value, set it to false
      localStorage.setItem("SETTING_"+id, false);
    }
    // set the checkbox to the value
    elem.checked = localStorage.getItem("SETTING_"+id) == "true";

    // add event listener
    elem.addEventListener('change', function() {
      // set the value in local storage
      localStorage.setItem("SETTING_"+id, elem.checked);
    });
  });

  

  
});