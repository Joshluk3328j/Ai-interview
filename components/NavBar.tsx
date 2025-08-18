"use client";

import Link from "next/link";
import Image from "next/image";

export default function NavBar() {
  return (
    <>
      <div className="flex justify-center items-center w-full p-6">
        <div className="flex flex-row items-center gap-4">
          <Link href="/">
            <Image
              src="/viewhire-logo.png"
              alt="ViewHire Logo"
              width={70}
              height={70}
              className="rounded-md"
            />
          </Link>
          <div className="bg-gradient-to-br from-sky-300 to-indigo-500 bg-clip-text">
            <p className="text-xl font-semibold text-transparent">
              ViewHire - Powered by RTAI (Real-Time Automated Interviewer)
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
