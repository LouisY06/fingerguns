import { Target, Cpu, Users, CheckCircle } from 'lucide-react';

export default function About() {
  return (
    <div className="bg-black">
      {/* Hero Section */}
      <section className="py-24 px-6 lg:px-8 bg-gradient-to-b from-black via-gray-950 to-black">
        <div className="max-w-5xl mx-auto text-center">
          <h1 className="h1-text text-white mb-6">
            Redefining Human-Computer Interaction
          </h1>
          <p className="body-text text-gray-300 max-w-3xl mx-auto">
            FingerGuns represents a breakthrough in natural user interfaces, bringing intuitive gesture-based controls to competitive gaming through advanced computer vision technology.
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-24 px-6 lg:px-8 bg-gray-950">
        <div className="max-w-5xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="w-12 h-12 bg-gray-800 flex items-center justify-center mb-6">
                <Target className="text-white" size={24} />
              </div>
              <h2 className="h2-text text-white mb-6">Our Mission</h2>
              <p className="body-text text-gray-300 mb-4">
                We believe that human-computer interaction should be as natural as possible. Traditional input devices like keyboards and mice create an artificial barrier between players and their games.
              </p>
              <p className="body-text text-gray-300">
                FingerGuns eliminates this barrier by leveraging computer vision and machine learning to recognize natural human movements, translating them into precise game controls without any specialized hardware.
              </p>
            </div>
            <div className="bg-black border border-gray-800 p-8">
              <blockquote className="border-l-4 border-white pl-6">
                <p className="body-text text-gray-300 italic mb-4">
                  &ldquo;Steve Jobs believed the best precision device is your finger. We took that philosophy further—why not eliminate the mouse entirely?&rdquo;
                </p>
                <cite className="body-text text-gray-500 not-italic">— FingerGuns Development Team</cite>
              </blockquote>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-24 px-6 lg:px-8 bg-black">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <div className="w-12 h-12 bg-gray-800 flex items-center justify-center mx-auto mb-6">
              <Cpu className="text-white" size={24} />
            </div>
            <h2 className="h2-text text-white mb-4">Advanced Technology Stack</h2>
            <p className="body-text text-gray-400 max-w-2xl mx-auto">
              Built on MediaPipe with optimization techniques inspired by NVIDIA&apos;s frame generation technology.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
            <div className="bg-gray-950 border border-gray-800 p-8">
              <h3 className="h4-text text-white mb-4">MediaPipe Integration</h3>
              <p className="body-text text-gray-400 mb-4">
                Multi-model computer vision pipeline processing hands, pose, and facial landmarks in parallel at 30 FPS.
              </p>
              <ul className="space-y-2">
                <li className="body-text text-sm text-gray-400 flex items-start">
                  <CheckCircle className="text-white mr-2 flex-shrink-0 mt-1" size={16} />
                  Dual 21-point hand tracking
                </li>
                <li className="body-text text-sm text-gray-400 flex items-start">
                  <CheckCircle className="text-white mr-2 flex-shrink-0 mt-1" size={16} />
                  468-point face mesh for head pose
                </li>
                <li className="body-text text-sm text-gray-400 flex items-start">
                  <CheckCircle className="text-white mr-2 flex-shrink-0 mt-1" size={16} />
                  33-point pose estimation for body lean
                </li>
              </ul>
            </div>

            <div className="bg-gray-950 border border-gray-800 p-8">
              <h3 className="h4-text text-white mb-4">NVIDIA-Inspired Interpolation</h3>
              <p className="body-text text-gray-400 mb-4">
                Vision pipeline produces movement deltas at 30 FPS. A 120 Hz cursor thread drains the delta backlog, applying micro-steps to fill gaps between frames.
              </p>
              <ul className="space-y-2">
                <li className="body-text text-sm text-gray-400 flex items-start">
                  <CheckCircle className="text-white mr-2 flex-shrink-0 mt-1" size={16} />
                  Delta backlog accumulation (30 FPS input)
                </li>
                <li className="body-text text-sm text-gray-400 flex items-start">
                  <CheckCircle className="text-white mr-2 flex-shrink-0 mt-1" size={16} />
                  Fractional drain per tick (120 Hz output)
                </li>
                <li className="body-text text-sm text-gray-400 flex items-start">
                  <CheckCircle className="text-white mr-2 flex-shrink-0 mt-1" size={16} />
                  ~8-10ms latency, no jumps or overshoot
                </li>
              </ul>
            </div>
          </div>

          {/* Math Explanation */}
          <div className="bg-gray-950 border border-gray-800 p-8">
            <h3 className="h4-text text-white mb-4">Gradient Descent Analogy</h3>
            <p className="body-text text-gray-400 mb-4">
              Each 30 FPS vision frame adds a movement delta to the backlog. The 120 Hz cursor thread exponentially drains this backlog by applying a fraction each tick:
            </p>
            <div className="bg-black p-6 rounded font-mono text-sm text-gray-300 mb-4 overflow-x-auto">
              <div className="mb-2">backlog<sub>t+1</sub> = backlog<sub>t</sub> + new_delta  <span className="text-gray-500">{'// 30 FPS'}</span></div>
              <div className="mb-2">movement = α · backlog<sub>t</sub>  <span className="text-gray-500">{'// 120 Hz'}</span></div>
              <div className="mb-2">backlog<sub>t+1</sub> = backlog<sub>t</sub> - movement</div>
              <div className="text-gray-500 text-xs mt-4">
                where α = 0.15 (drain rate per tick)
              </div>
            </div>
            <p className="body-text text-gray-400 mb-4">
              Like gradient descent exponentially reduces error, the cursor thread exponentially drains the backlog vector. Each tick subtracts a fraction of the remaining distance, creating micro-steps that transform discrete 30 FPS motion into continuous 120 Hz smoothness.
            </p>
            <p className="body-text text-gray-400">
              Inspired by NVIDIA DLSS 3&apos;s frame generation philosophy: decouple input rate (30 FPS vision) from output rate (120 Hz cursor). The result is near-instant responsiveness with buttery-smooth motion—no prediction, just intelligent backlog management.
            </p>
          </div>
        </div>
      </section>

      {/* Key Features Section */}
      <section className="py-24 px-6 lg:px-8 bg-gray-950">
        <div className="max-w-5xl mx-auto">
          <h2 className="h2-text text-white mb-12 text-center">What Sets Us Apart</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-black border border-gray-800 p-6">
              <h4 className="h4-text text-white mb-3">No Special Hardware</h4>
              <p className="body-text text-sm text-gray-400">
                Works with any standard webcam—no need for expensive motion tracking equipment.
              </p>
            </div>
            <div className="bg-black border border-gray-800 p-6">
              <h4 className="h4-text text-white mb-3">Low Latency</h4>
              <p className="body-text text-sm text-gray-400">
                Optimized processing pipeline ensures responsive controls suitable for competitive play.
              </p>
            </div>
            <div className="bg-black border border-gray-800 p-6">
              <h4 className="h4-text text-white mb-3">Customizable</h4>
              <p className="body-text text-sm text-gray-400">
                Adjust sensitivity, thresholds, and gesture mappings to match your playstyle.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-24 px-6 lg:px-8 bg-black">
        <div className="max-w-5xl mx-auto text-center">
          <div className="w-12 h-12 bg-gray-800 flex items-center justify-center mx-auto mb-6">
            <Users className="text-white" size={24} />
          </div>
          <h2 className="h2-text text-white mb-6">Built by Engineers</h2>
          <p className="body-text text-gray-300 max-w-3xl mx-auto mb-8">
            FingerGuns was developed by a team of computer vision engineers and gaming enthusiasts who wanted to push the boundaries of what&apos;s possible with modern machine learning frameworks.
          </p>
          <p className="body-text text-gray-400 max-w-3xl mx-auto">
            What started as a hackathon thought experiment has evolved into a fully-featured control system that demonstrates the potential of gesture-based interfaces in gaming.
          </p>
        </div>
      </section>
    </div>
  );
}

