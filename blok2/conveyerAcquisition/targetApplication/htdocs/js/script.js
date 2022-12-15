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

    if(id == "stream"){
      elem.addEventListener('change', function() {
        if(elem.checked){
          document.getElementById("stream").style.display = "block";
        }else{
          document.getElementById("stream").style.display = "none";
        }
      });
    }
  });

  /**
   * turn of stream if not checked
   */

  if(localStorage.getItem("SETTING_stream") == "false"){
    document.getElementById("stream").style.display = "none";
  }

  /**
   * set all loops for fetching data
   */
  let interval = setInterval(async ()=>{
    if (localStorage.getItem("SETTING_stream") == "true") {
      // update image src to get new image
      document.getElementById("stream").src = "";
      // update image src to get new image
      document.getElementById("stream").src = "/api/classifications/latest/image/";
    }

    // update last classification list
    let response = await fetch("/api/classifications/latest");

    let data = await response.json();
    console.log(data);
    if (data.length > 0) {
      data.forEach((classification)=>{
        classification.classification.forEach((tinyClassification)=>{
          // add li to the list
          let li = document.createElement("p");
          let time = new Date(classification.timestamp);
          li.innerHTML = time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds() + " - " + tinyClassification.class + " - " + tinyClassification.confidence;
          document.getElementById("lastClassifications").prepend(li);
        })
      });
    } else {
      // add li to the list
      let li = document.createElement("p");
      li.innerHTML = "No classifications yet";
      document.getElementById("lastClassifications").prepend(li);
    }
    
  },
    ((localStorage.getItem("SETTING_interval") == false)? 1000 : 1000/5) // 1 or 5 fps
  ); 


});