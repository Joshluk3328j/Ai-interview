"use client";
import { useEffect, useRef } from "react";
import InteractiveAvatar from "@/components/InteractiveAvatar";

export default function App() {
  const myVideoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });
        if (myVideoRef.current) {
          myVideoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error accessing camera:", err);
      }
    }
    startCamera();
  }, []);

  return (
    <div className="w-screen h-screen flex flex-col relative bg-black">
      {/* Avatar main video area */}
      <div className="w-[900px] flex flex-col items-start justify-start gap-5 mx-auto pt-4 pb-20 relative">
        <div className="w-full">
          <InteractiveAvatar />
        </div>

        {/* Camera overlay ON TOP of avatar */}
        <video
          ref={myVideoRef}
          autoPlay
          muted
          playsInline
          className="absolute top-10 right-5 w-40 h-28 rounded-xl shadow-lg border-2 border-white"
        />
      </div>
    </div>
  );
}
