$(document).ready(function () {
  $(".text").textillate({
    loop: true,
    sync: true,
    in: { effect: "bounceIn" },
    out: { effect: "bounceOut" },
  });

  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 640,
    height: 200,
    style: "ios9",
    amplitude: 1,
    speed: 0.3,
    autostart: true,
  });

  $(".siri-message").textillate({
    loop: true,
    sync: true,
    in: { effect: "fadeInUp", sync: true },
    out: { effect: "fadeOutUp", sync: true },
  });

  $("#MicBtn").click(function () {
    eel.playAssistantSound();
    $("#oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);

    
    eel.allCommands()();
  });

document.addEventListener("DOMContentLoaded", function () {
  let queryInput = document.getElementById("queryInput");

  queryInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      let query = queryInput.value;
      queryInput.value = ""; 

      eel.send_query_to_python(query)(function (response) {
        console.log("Response from Python:", response);
        displayResponse(response);
      });
    }
  });
});

function displayResponse(response) {
  let responseContainer = document.getElementById("responseContainer");
  responseContainer.innerHTML = `<p class="response-text">${response}</p>`;
}

});
