async function getHelp() {
  const userInput = document.getElementById('userInput').value;
  const responseBox = document.getElementById('response');

  responseBox.innerHTML = "Loading...";

  const response = await fetch("http://127.0.0.1:5000/get-help", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: userInput })
  });

  const data = await response.json();
  responseBox.innerHTML = `<strong>AI Suggestion:</strong><br>${data.reply}`;
}
