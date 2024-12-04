export const createWebSocket = (url) => {
  const socket = new WebSocket(url);

  socket.onopen = () => {
    console.log("WebSocket connection opened.");
  };

  socket.onmessage = (event) => {
    console.log("Message received: ", event.data);
  };

  socket.onclose = () => {
    console.log("WebSocket connection closed.");
  };

  socket.onerror = (error) => {
    console.error("WebSocket error: ", error);
  };

  return socket;
};
