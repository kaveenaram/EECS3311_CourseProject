import { useState } from "react";

const AI_URL = "http://localhost:5000/api/chat";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  async function sendMessage() {
    if (!input.trim()) return;

    const userMsg = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    try {
      const res = await fetch(AI_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input })
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        { text: data.reply, sender: "ai" }
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { text: "AI error", sender: "ai" }
      ]);
    }
  }

  return (
    <>
      <button
        onClick={() => setOpen(!open)}
        style={{
          position: "fixed",
          bottom: "20px",
          right: "20px"
        }}
      >
        💬
      </button>

      {open && (
        <div style={{
          position: "fixed",
          bottom: "80px",
          right: "20px",
          width: "300px",
          height: "400px",
          border: "1px solid black",
          background: "white",
          display: "flex",
          flexDirection: "column"
        }}>
          <div style={{ flex: 1, overflowY: "scroll" }}>
            {messages.map((m, i) => (
              <p key={i}>
                <b>{m.sender}:</b> {m.text}
              </p>
            ))}
          </div>

          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      )}
    </>
  );

  
}