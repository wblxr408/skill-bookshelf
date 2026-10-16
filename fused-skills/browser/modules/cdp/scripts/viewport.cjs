#!/usr/bin/env node
const http = require("http");
const WebSocket = require("ws");

const width = Number.parseInt(process.argv[2] ?? "", 10);
const height = Number.parseInt(process.argv[3] ?? "", 10);

if (!Number.isInteger(width) || !Number.isInteger(height) || width <= 0 || height <= 0) {
  console.error("Usage: viewport.cjs <width> <height>");
  process.exit(1);
}

function getTargets() {
  return new Promise((resolve, reject) => {
    http
      .get("http://localhost:9222/json", (response) => {
        let data = "";
        response.on("data", (chunk) => (data += chunk));
        response.on("end", () => resolve(JSON.parse(data)));
      })
      .on("error", reject);
  });
}

(async () => {
  const targets = await getTargets();
  const page = targets.find((target) => target.type === "page");
  if (!page) throw new Error("No active page found");

  const socket = new WebSocket(page.webSocketDebuggerUrl);
  socket.on("open", () => {
    socket.send(
      JSON.stringify({
        id: 1,
        method: "Emulation.setDeviceMetricsOverride",
        params: {
          width,
          height,
          deviceScaleFactor: 1,
          mobile: width <= 900,
          screenWidth: width,
          screenHeight: height,
        },
      }),
    );
  });
  socket.on("message", (data) => {
    const message = JSON.parse(data);
    if (message.id !== 1) return;
    socket.close();
    console.log(JSON.stringify({ width, height, mobile: width <= 900 }));
  });
  socket.on("error", (error) => {
    console.error(error.message);
    process.exit(1);
  });
})();
