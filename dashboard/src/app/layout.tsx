import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Regime Detection System 🚀",
  description: "Live CI/CD Demo Deployment",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-slate-950 text-slate-200 overflow-x-hidden`}
      >
        <div className="flex min-h-screen max-w-[100vw]">
          <Sidebar />

          <div className="flex-1 w-full overflow-y-auto">

            {/* 🚀 DEMO BANNER */}
            <div className="bg-green-600 text-white text-center py-2 font-semibold">
              🚀 Deployed via Jenkins and  CI/CD (Live Demo)
            </div>

            {children}
          </div>
        </div>
      </body>
    </html>
  );
}