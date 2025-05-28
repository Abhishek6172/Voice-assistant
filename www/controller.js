
 $(document).ready(function () {
  console.log("Controller ready.");
});


main.js


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
    
    // Hide oval section and show SiriWave
    document.getElementById("oval").hidden = true;
    document.getElementById("SiriWave").hidden = false;

    // Pause and hide the video
    const video = document.getElementById("bgVideo");
    if (!video.paused) {
      video.pause();
      video.style.display = "none";
    }

    eel.allCommands()();
  });

  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
    $(".siri-message").text(message);
    $(".siri-message").textillate("start");
  }

  // Expose ShowHood function to Python
  eel.expose(ShowHood);
  function ShowHood() {
    document.getElementById("oval").hidden = false;
    document.getElementById("SiriWave").hidden = true;
    const video = document.getElementById("bgVideo");
    // video.style.display = "block";
    video.play();
  }
});

