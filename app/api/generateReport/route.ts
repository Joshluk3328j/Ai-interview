import { NextResponse } from "next/server";
import { spawn } from "child_process";

export async function POST(req: Request) {
  try {
    const { conversation } = await req.json();
    if (!conversation) {
      return NextResponse.json(
        { error: "No conversation data provided" },
        { status: 400 }
      );
    }

    return new Promise((resolve) => {
      const py = spawn("python3", ["generateReport.py"], {
        cwd: process.cwd(),
      });

      let stdoutOutput: Uint8Array[] = [];
      let errorOutput = "";

      // Send JSON to Python
      py.stdin.write(JSON.stringify(conversation));
      py.stdin.end();

      py.stdout.on("data", (data) => {
        stdoutOutput.push(data);
      });

      py.stderr.on("data", (data) => {
        errorOutput += data.toString();
      });

      py.on("close", (code) => {
        if (code !== 0) {
          console.error("Python script failed:", errorOutput);
          resolve(
            NextResponse.json(
              {
                error: "Python script failed",
                details: errorOutput || "No error output",
              },
              { status: 500 }
            )
          );
          return;
        }

        try {
          const pdfBuffer = Buffer.concat(stdoutOutput);
          resolve(
            new NextResponse(pdfBuffer, {
              headers: {
                "Content-Type": "application/pdf",
                "Content-Disposition":
                  "attachment; filename=interview_report.pdf",
              },
            })
          );
        } catch (err) {
          console.error("Failed to return PDF:", err);
          resolve(
            NextResponse.json(
              { error: "Failed to return PDF", details: String(err) },
              { status: 500 }
            )
          );
        }
      });
    });
  } catch (err) {
    console.error("API error:", err);
    return NextResponse.json(
      { error: "Internal Server Error", details: String(err) },
      { status: 500 }
    );
  }
}
