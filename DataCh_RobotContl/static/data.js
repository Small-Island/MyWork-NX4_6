var ws;
ws = new WebSocket("ws://localhost:8888/websocket");
ws.onmessage = function (ev) {
    log(ev);
}
const sora = Sora.connection("wss://sora.ikeilabsora.0am.jp/signaling", debug);
const sendrecv = sora.recvonly("rabbit-go@twincamleft", null, null);
dataConnection.on("push", (message, transportType) => {
    ws.send(message.data.Deg);
});