import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "NOVA – Personal AI Operating System",
  description: "Think. Remember. Orchestrate. Execute. Autonomous Personal AI Operating System powered by NVIDIA Nemotron & Nebius Token Factory.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}

