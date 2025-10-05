import type { Metadata } from "next";
import "./globals.css";
import Navigation from "@/components/Navigation";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  metadataBase: new URL('http://localhost:3000'),
  title: "FingerGuns - Control CS:GO with Hand Gestures",
  description: "Revolutionary computer vision technology enabling natural hand gesture, body leaning, and head tracking controls for Counter-Strike: Global Offensive.",
  icons: {
    icon: "/fingergunslogo.png",
    shortcut: "/fingergunslogo.png",
    apple: "/fingergunslogo.png",
  },
  openGraph: {
    title: "FingerGuns - Control CS:GO with Hand Gestures",
    description: "Revolutionary computer vision technology enabling natural hand gesture, body leaning, and head tracking controls for Counter-Strike: Global Offensive.",
    images: ["/fingergunslogo.png"],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "FingerGuns - Control CS:GO with Hand Gestures",
    description: "Revolutionary computer vision technology enabling natural hand gesture, body leaning, and head tracking controls for Counter-Strike: Global Offensive.",
    images: ["/fingergunslogo.png"],
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
