import { useState } from 'react';
import { FileUploader } from './components/FileUploader';
import { HarViewer } from './components/HarViewer';
import { HarData } from './types';
import { Shield, Github, Activity } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function App() {
  const [harData, setHarData] = useState<HarData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileLoaded = (data: HarData) => {
    setHarData(data);
    setError(null);
  };

  const handleError = (msg: string) => {
    setError(msg);
    setHarData(null);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="h-16 border-b border-zinc-800 bg-zinc-950/50 backdrop-blur-xl sticky top-0 z-50 px-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center">
            <Activity className="w-5 h-5 text-zinc-950" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight">HAR Inspector</h1>
            <p className="text-[10px] text-zinc-500 uppercase tracking-widest font-bold">Network Archive Tool</p>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="hidden md:flex items-center gap-2 text-xs text-zinc-500">
            <Shield className="w-3 h-3" />
            Client-side only
          </div>
          <a 
            href="https://github.com" 
            target="_blank" 
            rel="noreferrer"
            className="p-2 text-zinc-500 hover:text-white transition-colors"
          >
            <Github className="w-5 h-5" />
          </a>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 relative">
        <AnimatePresence mode="wait">
          {!harData ? (
            <motion.div
              key="uploader"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="p-6"
            >
              <div className="max-w-4xl mx-auto text-center mb-12 mt-12">
                <h2 className="text-4xl md:text-5xl font-bold mb-4 tracking-tight bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent">
                  Analyze and Modify Network Logs
                </h2>
                <p className="text-zinc-400 text-lg max-w-2xl mx-auto">
                  A powerful, privacy-focused tool to inspect, filter, and convert HTTP Archive (HAR) files directly in your browser.
                </p>
              </div>

              <FileUploader onFileLoaded={handleFileLoaded} onError={handleError} />

              {error && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="max-w-md mx-auto mt-8 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-500 text-sm text-center"
                >
                  {error}
                </motion.div>
              )}
            </motion.div>
          ) : (
            <motion.div
              key="viewer"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <HarViewer 
                data={harData} 
                onUpdate={setHarData} 
                onReset={() => setHarData(null)} 
              />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      {!harData && (
        <footer className="p-8 border-t border-zinc-900 text-center text-zinc-600 text-xs">
          <p>© 2026 HAR Inspector. Built for developers.</p>
        </footer>
      )}
    </div>
  );
}
