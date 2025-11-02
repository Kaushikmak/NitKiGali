const socket = new WebSocket("ws://localhost:8000/ws/test/");

socket.onopen = () => {
  console.log("WebSocket connected!");
  socket.send(JSON.stringify({ message: "Hello from client" }));
};

socket.onmessage = e => console.log("Received:", e.data);

socket.onclose = () => console.log("WebSocket disconnected");
socket.onerror = e => console.error("WebSocket error:", e);
