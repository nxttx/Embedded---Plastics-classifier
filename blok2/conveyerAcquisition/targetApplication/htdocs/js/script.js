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
  async function loop(){
    if (localStorage.getItem("SETTING_stream") == "true") {
      try {
        let request = await fetch("/api/classifications/latest/image")
        let blob = await request.blob();
        let url = URL.createObjectURL(blob);
        document.getElementById("image-stream").src = url;
      } catch (error) {
        console.error(error);
      }
    }

    // update last classification list
    try {
      let response = await fetch("/api/classifications/latest");
  
      let data = await response.json();
  
      data.classification.forEach((classification)=>{
        let content = document.createElement("p");
        let time = new Date(data.timestamp);
  
        content.innerHTML = time.getHours() + ":" ;
        content.innerHTML += time.getMinutes() + ":" ;
        content.innerHTML += time.getSeconds() + " > " ;
        content.innerHTML += classification.class + " - " ;
  
        let confidence = Number(classification.confidence)*100;
        // round to 2 decimals
        confidence = Math.round(confidence * 100) / 100;
        content.innerHTML += (confidence + "%");
  
        // add to #lastClassifications as last child
        document.getElementById("lastClassifications").appendChild(content);
        
      })
    } catch (error) {
      console.error(error);
    }


    setTimeout(loop,
      ((localStorage.getItem("SETTING_framerate") == "false")? 1000 : 1000/5) // 1 or 5 fps
    );
  }

  loop();

  /**
   * command input control
   */
  document.getElementById("command").
  // if keypress is enter
  addEventListener("keyup", async function(event) {
    if (event.keyCode === 13) {
      // lower case the input
      this.value = this.value.toLowerCase();

      // check what the command is
      switch (this.value) {
        case "clear":
          // clear the last classifications
          document.getElementById("lastClassifications").innerHTML = "";
          break;
        case "help":
          // show help
          let help = document.createElement("p");

          help.innerHTML = "<br>--- HELP ---------- <br>";
          help.innerHTML += "clear <br>&nbsp; &nbsp;Clear the last classifications <br>";
          help.innerHTML += "help <br>&nbsp; &nbsp;Show this help <br>";
          help.innerHTML += "version <br>&nbsp; &nbsp;Show the version of the application <br><br>";

          document.getElementById("lastClassifications").appendChild(help);
          break;
        case "version":
          // show version
          let version = document.createElement("p");
          version.innerHTML = "Version: 1.0.0";
          document.getElementById("lastClassifications").appendChild(version);
          break;
        case "hello kitty":
          // add confettiJS script to the page
          // check if script is already added
          if(document.getElementById("confetti-script") == null){
            let script = document.createElement("script");
            script.src = 'js/confetty.min.js';
            script.id = "confetti-script";
            document.body.appendChild(script);
          }
          // show confetti
          setTimeout(function(){
            displayConfetty(5000)
          }, 500);
          break;
        default:
          // show error
          let error = document.createElement("p");
          error.innerHTML = "ERROR: Command not found";
          document.getElementById("lastClassifications").appendChild(error);
          break;
      }

      // clear the input
      this.value = "";
    } 
  });


});