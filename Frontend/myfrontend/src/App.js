import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi! Ask me about crops or seasons." },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { from: "user", text: input };
    setMessages((msgs) => [...msgs, userMsg]);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      setMessages((msgs) => [...msgs, { from: "bot", text: data.response }]);
    } catch (err) {
      setMessages((msgs) => [...msgs, { from: "bot", text: "Error connecting to server." }]);
    }
    setInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h2>The Oasis Chatbot</h2>
      <div
        style={{
          border: "1px solid #ccc",
          height: 400,
          padding: 10,
          overflowY: "auto",
          marginBottom: 10,
          backgroundColor: "#fafafa",
        }}
      >
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              textAlign: msg.from === "user" ? "right" : "left",
              margin: "10px 0",
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "8px 15px",
                borderRadius: 20,
                backgroundColor: msg.from === "user" ? "#007bff" : "#e5e5ea",
                color: msg.from === "user" ? "white" : "black",
                maxWidth: "70%",
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message..."
        style={{ width: "80%", padding: 10, fontSize: 16 }}
      />
      <button onClick={sendMessage} style={{ padding: "10px 20px", fontSize: 16, marginLeft: 10 }}>
        Send
      </button>
    </div>
  );
}

export default App;
