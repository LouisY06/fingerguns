import Link from 'next/link';
import { Github } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-black border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand & Description */}
          <div className="md:col-span-2">
            <Link href="/" className="inline-block mb-4">
              <span className="brand-text text-2xl text-white">FingerGuns</span>
            </Link>
            <p className="body-text text-sm text-gray-400 max-w-md">
              Revolutionary computer vision technology enabling natural hand gesture and head tracking controls for Counter-Strike: Global Offensive.
            </p>
            <div className="flex space-x-4 mt-6">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white transition-smooth"
                aria-label="GitHub"
              >
                <Github size={20} />
              </a>
            </div>
          </div>

          {/* Product Links */}
          <div>
            <h4 className="body-text font-semibold text-white mb-4">Product</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="body-text text-sm text-gray-400 hover:text-white transition-smooth">
                  Features
                </Link>
              </li>
              <li>
                <Link href="/docs" className="body-text text-sm text-gray-400 hover:text-white transition-smooth">
                  Documentation
                </Link>
              </li>
              <li>
                <Link href="/download" className="body-text text-sm text-gray-400 hover:text-white transition-smooth">
                  Download
                </Link>
              </li>
            </ul>
          </div>

          {/* Support Links */}
          <div>
            <h4 className="body-text font-semibold text-white mb-4">Support</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/about" className="body-text text-sm text-gray-400 hover:text-white transition-smooth">
                  About
                </Link>
              </li>
              <li>
                <Link href="/docs" className="body-text text-sm text-gray-400 hover:text-white transition-smooth">
                  Help Center
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="pt-8 border-t border-gray-800">
          <p className="body-text text-sm text-gray-500 text-center">
            © {new Date().getFullYear()} FingerGuns. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}

