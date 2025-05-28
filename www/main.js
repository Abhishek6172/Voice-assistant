$(document).ready(function () {
  const siriWave = new SiriWave({
    container: document.getElementById("wave-canvas"),
    width: window.innerWidth,
    height: window.innerHeight * 0.4,
    style: "ios9",
    amplitude: 1.5,
    speed: 0.2,
    autostart: true,
  });

  window.addEventListener("resize", () => {
    siriWave.set({
      width: window.innerWidth,
      height: window.innerHeight * 0.4,
    });
  });

  let isResponding = false;
  let hasShifted = false;
  $("#MicBtn").click(function () {
    document.getElementById("oval").hidden = true;
    document.getElementById("SiriWave").hidden = false;

    const video = document.getElementById("bgVideo");
    if (!video.paused) {
      video.pause();
      video.style.display = "none";
    }

    isResponding = true;
    hasShifted = false;
    document.getElementById("siri-messages").innerHTML = "";
    $("#listening-indicator").text("Listening...").fadeIn();

    eel.startListening();
  });
  eel.expose(DisplayConversation);
  function DisplayConversation(userText, assistantText) {
    const container = document.getElementById("siri-messages");
    if (!hasShifted && userText && assistantText) {
      $("#listening-indicator").fadeOut(() => {
        document.getElementById("siri-container").classList.add("moved");
        hasShifted = true;
      });
    }
    const statusMessages = [
      "listening...",
      "recognizing...",
      "timeout: no speech detected.",
      "thinking...",
    ];

    if (userText && !statusMessages.includes(userText.toLowerCase())) {
      const user = document.createElement("p");
      user.innerText = `You: ${userText}`;
      user.style.color = "white";
      container.appendChild(user);
    }

    if (assistantText && !statusMessages.includes(assistantText.toLowerCase())) {
      const ai = document.createElement("p");
      ai.innerText = `Assistant: ${assistantText}`;
      ai.style.color = "cyan";
      ai.style.textShadow = "0 0 10px cyan";
      container.appendChild(ai);
    }

    container.scrollTop = container.scrollHeight;
  }
  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
    $("#listening-indicator").text(message).fadeIn();
  }
  eel.expose(ShowHood);
  function ShowHood() {
    document.getElementById("oval").hidden = false;
    document.getElementById("SiriWave").hidden = true;

    const video = document.getElementById("bgVideo");
    video.style.display = "block";
    video.play().catch((e) => console.error("Video play failed:", e));

    isResponding = false;
    hasShifted = false;
    $("#siri-container").removeClass("moved");
    $("#listening-indicator").hide();
    $("#siri-messages").innerHTML = "";
  }
  $(document).keydown(function (e) {
    if (e.key === "x" || e.key === "X") {
      if (isResponding) {
        eel.stopSpeaking();
        ShowHood();
      } else {
        $("#MicBtn").click();
      }
    }
  });
  eel.welcome();
});
