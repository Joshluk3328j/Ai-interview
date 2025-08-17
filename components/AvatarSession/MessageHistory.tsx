import React, { useEffect, useRef, useState } from "react";
import { useMessageHistory, MessageSender } from "../logic";

export const MessageHistory: React.FC = () => {
  const { messages } = useMessageHistory();
  const containerRef = useRef<HTMLDivElement>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const container = containerRef.current;
    if (!container || messages.length === 0) return;
    container.scrollTop = container.scrollHeight;
  }, [messages]);

  const exportToPDF = async () => {
    setIsLoading(true);
    try {
      const conversation = messages.map((msg) => ({
        role: msg.sender === MessageSender.AVATAR ? "assistant" : "user",
        content: msg.content,
      }));
      console.log("Conversation:", JSON.stringify(conversation));

      const response = await fetch("/api/generateReport", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversation }),
      });

      if (!response.ok) {
        const errorData = await response.text();
        console.error("API Error:", response.status, errorData);
        throw new Error(`Failed to generate report: ${response.status} ${errorData}`);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "interview_report.pdf";
      a.click();
      URL.revokeObjectURL(url);
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      console.error("Error generating PDF:", error);
      alert(`Failed to generate PDF report: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <div
        ref={containerRef}
        className="w-[600px] overflow-y-auto flex flex-col gap-2 px-2 py-2 text-white self-center max-h-[150px]"
      >
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex flex-col gap-1 max-w-[350px] ${
              message.sender === MessageSender.CLIENT
                ? "self-end items-end"
                : "self-start items-start"
            }`}
          >
            <p className="text-xs text-zinc-400">
              {message.sender === MessageSender.AVATAR ? "Avatar" : "You"}
            </p>
            <p className="text-sm">{message.content}</p>
          </div>
        ))}
      </div>

      <button
        onClick={exportToPDF}
        disabled={isLoading}
        className={`bg-blue-600 text-white px-3 py-1 rounded-md self-center ${
          isLoading ? "opacity-50 cursor-not-allowed" : ""
        }`}
      >
        {isLoading ? "Generating..." : "Generate PDF Report"}
      </button>
    </div>
  );
};