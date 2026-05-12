import React, { useCallback } from 'react';
import { useDropzone, DropzoneOptions } from 'react-dropzone';
import { Upload, FileJson, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '../utils';

interface FileUploaderProps {
  onFileLoaded: (data: any) => void;
  onError: (error: string) => void;
}

export function FileUploader({ onFileLoaded, onError }: FileUploaderProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const json = JSON.parse(e.target?.result as string);
        if (!json.log || !json.log.entries) {
          throw new Error('Invalid HAR file format');
        }
        onFileLoaded(json);
      } catch (err) {
        onError(err instanceof Error ? err.message : 'Failed to parse HAR file');
      }
    };
    reader.onerror = () => onError('Failed to read file');
    reader.readAsText(file);
  }, [onFileLoaded, onError]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/json': ['.har', '.json'],
    },
    multiple: false,
  } as any);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-2xl mx-auto mt-20"
    >
      <div
        {...getRootProps()}
        className={cn(
          "relative group cursor-pointer rounded-2xl border-2 border-dashed transition-all duration-300 p-12 text-center",
          isDragActive 
            ? "border-emerald-500 bg-emerald-500/5" 
            : "border-zinc-800 hover:border-zinc-700 bg-zinc-900/50 hover:bg-zinc-900"
        )}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center gap-4">
          <div className={cn(
            "w-16 h-16 rounded-full flex items-center justify-center transition-colors",
            isDragActive ? "bg-emerald-500 text-white" : "bg-zinc-800 text-zinc-400 group-hover:bg-zinc-700"
          )}>
            <Upload className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-1">Drop your HAR file here</h3>
            <p className="text-zinc-500">or click to browse from your computer</p>
          </div>
          <div className="flex items-center gap-2 text-xs text-zinc-600 mt-4">
            <FileJson className="w-4 h-4" />
            <span>Supports .har and .json files</span>
          </div>
        </div>
      </div>
      
      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800 flex gap-3">
          <AlertCircle className="w-5 h-5 text-sky-500 shrink-0" />
          <div className="text-sm">
            <p className="font-medium text-zinc-300">Privacy First</p>
            <p className="text-zinc-500">Files are processed entirely in your browser. No data is ever uploaded to a server.</p>
          </div>
        </div>
        <div className="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800 flex gap-3">
          <AlertCircle className="w-5 h-5 text-amber-500 shrink-0" />
          <div className="text-sm">
            <p className="font-medium text-zinc-300">Security Note</p>
            <p className="text-zinc-500">HAR files can contain sensitive data like cookies and auth tokens. Be careful when sharing.</p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
