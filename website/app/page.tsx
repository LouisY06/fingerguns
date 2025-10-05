import Link from 'next/link';
import Image from 'next/image';
import { Hand, Eye, Zap, Download, FileText, Move, Target, Pointer } from 'lucide-react';

export default function Home() {
  return (
    <div className="bg-black">
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center justify-center px-6 lg:px-8 bg-gradient-to-b from-black via-gray-950 to-black">
        <div className="max-w-5xl mx-auto text-center">
          <div className="mb-8 flex justify-center">
            <Image 
              src="/fingergunslogo.png" 
              alt="FingerGuns Logo" 
              width={120} 
              height={120}
              className="w-24 h-24 md:w-32 md:h-32"
            />
          </div>
          <h1 className="h1-text text-white mb-6">
            Control CS:GO with Hand Gestures
          </h1>
          <p className="body-text text-gray-300 mb-12 max-w-3xl mx-auto">
            Transform natural hand movements, body leaning, and head tracking into precise game controls using computer vision and MediaPipe technology.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/download"
              className="inline-flex items-center justify-center px-8 py-4 bg-white text-black body-text font-semibold hover:bg-gray-200 transition-smooth"
            >
              <Download className="mr-2" size={20} />
              Download Now
            </Link>
            <Link
              href="/docs"
              className="inline-flex items-center justify-center px-8 py-4 bg-transparent border-2 border-white text-white body-text font-semibold hover:bg-white hover:text-black transition-smooth"
            >
              <FileText className="mr-2" size={20} />
              Documentation
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-6 lg:px-8 bg-gray-950">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="h2-text text-white mb-4">Complete Control System</h2>
            <p className="body-text text-gray-400 max-w-2xl mx-auto">
              Four-layer gesture recognition combining dual-hand tracking, body pose estimation, and NVIDIA-inspired motion interpolation.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Feature 1 */}
            <div className="bg-black border border-gray-800 p-6 transition-smooth hover:border-gray-600">
              <div className="w-12 h-12 bg-gray-800 flex items-center justify-center mb-4">
                <Pointer className="text-white rotate-90 scale-y-[-1]" size={24} />
              </div>
              <h3 className="h4-text text-white mb-3">Finger Gun Gesture</h3>
              <p className="body-text text-sm text-gray-400">
                Right hand controls aiming with index finger tracking. Natural thumb-down motion triggers firing.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-black border border-gray-800 p-6 transition-smooth hover:border-gray-600">
              <div className="w-12 h-12 bg-gray-800 flex items-center justify-center mb-4">
                <Hand className="text-white" size={24} />
              </div>
              <h3 className="h4-text text-white mb-3">Action Gestures</h3>
              <p className="body-text text-sm text-gray-400">
                Left hand palm recognition for crouch and jump commands. Intuitive finger counting system.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-black border border-gray-800 p-6 transition-smooth hover:border-gray-600">
              <div className="w-12 h-12 bg-gray-800 flex items-center justify-center mb-4">
                <Move className="text-white" size={24} />
              </div>
              <h3 className="h4-text text-white mb-3">Body Movement</h3>
              <p className="body-text text-sm text-gray-400">
                Head pose and body lean detection for WASD controls. Hands-free character navigation.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-black border border-gray-800 p-6 transition-smooth hover:border-gray-600">
              <div className="w-12 h-12 bg-gray-800 flex items-center justify-center mb-4">
                <Zap className="text-white" size={24} />
              </div>
              <h3 className="h4-text text-white mb-3">High-Fidelity Interpolation</h3>
              <p className="body-text text-sm text-gray-400">
                NVIDIA DLSS-inspired frame generation. 120 FPS cursor output from 30 FPS tracking for fluid motion.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Demo Section */}
      <section className="py-24 px-6 lg:px-8 bg-black">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="h2-text text-white mb-4">See It In Action</h2>
            <p className="body-text text-gray-400">
              Watch how FingerGuns transforms natural gestures into precise game controls.
            </p>
          </div>

          {/* Video Placeholder */}
          <div className="aspect-video bg-gray-900 border border-gray-800 flex items-center justify-center">
            <div className="text-center">
              <div className="w-20 h-20 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
                <div className="w-0 h-0 border-l-[20px] border-l-white border-t-[12px] border-t-transparent border-b-[12px] border-b-transparent ml-1"></div>
              </div>
              <p className="body-text text-gray-500">Demo video coming soon</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-6 lg:px-8 bg-gray-950">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="h2-text text-white mb-6">Ready to Transform Your Gameplay?</h2>
          <p className="body-text text-gray-300 mb-8 max-w-2xl mx-auto">
            Download FingerGuns today and experience Counter-Strike: Global Offensive like never before. Setup takes less than 5 minutes.
          </p>
          <Link
            href="/download"
            className="inline-flex items-center justify-center px-10 py-5 bg-white text-black body-text font-semibold hover:bg-gray-200 transition-smooth"
          >
            Get Started Now
          </Link>
        </div>
      </section>
    </div>
  );
}
