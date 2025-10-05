import { Download, Github, FileText, AlertCircle } from 'lucide-react';
import Link from 'next/link';

export default function DownloadPage() {
  return (
    <div className="bg-black">
      {/* Hero Section */}
      <section className="py-24 px-6 lg:px-8 bg-gradient-to-b from-black via-gray-950 to-black min-h-[80vh] flex items-center">
        <div className="max-w-5xl mx-auto text-center w-full">
          <h1 className="h1-text text-white mb-6">
            Download FingerGuns
          </h1>
          <p className="body-text text-gray-300 max-w-3xl mx-auto mb-12">
            Get started with gesture-based CSGO controls in minutes. Choose your preferred download method below.
          </p>

          {/* Download Options */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Direct Download */}
            <div className="bg-gray-950 border border-gray-800 p-8 text-left">
              <div className="w-12 h-12 bg-gray-800 flex items-center justify-center mb-6">
                <Download className="text-white" size={24} />
              </div>
              <h3 className="h3-text text-white mb-4">Direct Download</h3>
              <p className="body-text text-sm text-gray-400 mb-6">
                Download the latest stable release as a ready-to-run package. Includes all dependencies and setup instructions.
              </p>
              <button 
                disabled
                className="w-full py-4 bg-gray-800 text-gray-500 body-text font-semibold cursor-not-allowed"
              >
                Coming Soon
              </button>
              <p className="body-text text-xs text-gray-500 mt-3 text-center">
                Version 1.0.0 • Cross-platform
              </p>
            </div>

            {/* GitHub Download */}
            <div className="bg-gray-950 border border-gray-800 p-8 text-left">
              <div className="w-12 h-12 bg-gray-800 flex items-center justify-center mb-6">
                <Github className="text-white" size={24} />
              </div>
              <h3 className="h3-text text-white mb-4">Build from Source</h3>
              <p className="body-text text-sm text-gray-400 mb-6">
                Clone the repository and build from source. Perfect for developers who want to customize or contribute.
              </p>
              <button 
                disabled
                className="w-full py-4 bg-gray-800 text-gray-500 body-text font-semibold cursor-not-allowed"
              >
                View on GitHub
              </button>
              <p className="body-text text-xs text-gray-500 mt-3 text-center">
                Requires Python 3.8+ • Cross-platform
              </p>
            </div>
          </div>

          {/* Installation Notice */}
          <div className="mt-12 max-w-3xl mx-auto">
            <div className="bg-gray-950 border border-gray-800 p-6 flex items-start">
              <AlertCircle className="text-white mr-4 flex-shrink-0 mt-1" size={20} />
              <div className="text-left">
                <h4 className="h4-text text-white mb-2">Before You Install</h4>
                <p className="body-text text-sm text-gray-400">
                  FingerGuns is currently in active development. Public releases will be available soon. In the meantime, check out our documentation to learn more about the technology and features.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* System Requirements Quick Reference */}
      <section className="py-24 px-6 lg:px-8 bg-gray-950">
        <div className="max-w-5xl mx-auto">
          <h2 className="h2-text text-white mb-12 text-center">Recommended Requirements</h2>
          <p className="body-text text-gray-400 text-center max-w-2xl mx-auto mb-8">
            For optimal gesture tracking performance
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-black border border-gray-800 p-6 text-center">
              <h4 className="h4-text text-white mb-3">Operating System</h4>
              <p className="body-text text-sm text-gray-400">
                Windows 11 / macOS 12+
              </p>
            </div>
            <div className="bg-black border border-gray-800 p-6 text-center">
              <h4 className="h4-text text-white mb-3">Camera</h4>
              <p className="body-text text-sm text-gray-400">
                1080p at 60 FPS<br />
                <span className="text-gray-500 text-xs">(30 FPS works, 60 FPS better)</span>
              </p>
            </div>
            <div className="bg-black border border-gray-800 p-6 text-center">
              <h4 className="h4-text text-white mb-3">Hardware</h4>
              <p className="body-text text-sm text-gray-400">
                16 GB RAM<br />i7 / Ryzen 7 / M1+
              </p>
            </div>
          </div>
          <div className="text-center mt-8">
            <Link 
              href="/docs" 
              className="inline-flex items-center body-text text-sm text-gray-400 hover:text-white transition-smooth"
            >
              <FileText className="mr-2" size={16} />
              View Full Requirements & Setup Guide
            </Link>
          </div>
        </div>
      </section>

      {/* Next Steps */}
      <section className="py-24 px-6 lg:px-8 bg-black">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="h2-text text-white mb-6">What&apos;s Next?</h2>
          <p className="body-text text-gray-300 mb-8">
            While you wait for the official release, explore our comprehensive documentation to learn about gesture controls, calibration, and troubleshooting.
          </p>
          <Link
            href="/docs"
            className="inline-flex items-center justify-center px-8 py-4 bg-white text-black body-text font-semibold hover:bg-gray-200 transition-smooth"
          >
            <FileText className="mr-2" size={20} />
            Read Documentation
          </Link>
        </div>
      </section>
    </div>
  );
}

