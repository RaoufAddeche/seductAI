// 📄 src/components/ScoreBar.jsx
import React from "react";

function ScoreBar({ label, value, emoji }) {
  const percentage = Math.round((value || 0) * 100);

  return (
    <div style={{ marginBottom: "1rem" }}>
      <div style={{ fontWeight: "bold", marginBottom: "0.3rem" }}>
        {emoji} {label} : {percentage}%
      </div>
      <div style={{
        height: "12px",
        backgroundColor: "#ddd",
        borderRadius: "5px",
        overflow: "hidden"
      }}>
        <div style={{
          width: `${percentage}%`,
          backgroundColor: "#3498db",
          height: "100%",
          transition: "width 0.3s"
        }}></div>
      </div>
    </div>
  );
}

export default ScoreBar;
