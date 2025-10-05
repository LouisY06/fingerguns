import type { Metadata } from "next";
import "./globals.css";
import Navigation from "@/components/Navigation";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "FingerGuns - Control CS:GO with Hand Gestures",
  description: "Revolutionary computer vision technology enabling natural hand gesture, body leaning, and head tracking controls for Counter-Strike: Global Offensive.",
  icons: {
    icon: "/fingergunslogo.png",
    shortcut: "/fingergunslogo.png",
    apple: "/fingergunslogo.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <Navigation />
        <main className="min-h-screen pt-16">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
