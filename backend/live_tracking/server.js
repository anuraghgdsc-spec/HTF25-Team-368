const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const path = require("path");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Serve static files from this directory (so index.html and any local assets work)
app.use(express.static(path.join(__dirname)));

app.get('/', (req, res) => {
  // index.html lives next to this server.js file
  res.sendFile(path.join(__dirname, 'index.html'));
});

// In-memory store for sessions (for demo only)
const sessions = {}; // sessions[sessionId] = {path: [{lat,lon,t}], startSet:false, endSet:false}

io.on("connection", (socket) => {
  console.log("socket connected:", socket.id);

  // Join a session room
  socket.on("join-session", (sessionId) => {
    socket.join(sessionId);
    // Send current path for this session if exists
    if (sessions[sessionId]) {
      socket.emit("session-data", sessions[sessionId]);
    } else {
      sessions[sessionId] = { path: [], startSet: false, endSet: false, startedAt: null, endedAt: null };
    }
  });

  // Receive location update from client
  socket.on("location-update", ({ sessionId, lat, lon, timestamp }) => {
    if (!sessionId) return;
    const s = sessions[sessionId] || (sessions[sessionId] = { path: [], startSet: false, endSet: false, startedAt: null, endedAt: null });

    const point = { lat, lon, t: timestamp || Date.now() };
    s.path.push(point);
    if (!s.startSet) {
      s.startSet = true;
      s.startedAt = point.t;
    }
    s.endedAt = point.t;

    // Broadcast the new point to everyone in the session (including origin)
    io.to(sessionId).emit("new-point", point);
  });

  // Optional: mark session as finished by client
  socket.on("finish-session", ({ sessionId }) => {
    if (!sessions[sessionId]) return;
    sessions[sessionId].finished = true;
    io.to(sessionId).emit("session-finished", sessions[sessionId]);
  });

  socket.on("disconnect", () => {
    // nothing special for demo
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
