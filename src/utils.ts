import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatBytes(bytes: number, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

export function getStatusColor(status: number) {
  if (status >= 200 && status < 300) return 'text-emerald-500';
  if (status >= 300 && status < 400) return 'text-sky-500';
  if (status >= 400 && status < 500) return 'text-amber-500';
  if (status >= 500) return 'text-rose-500';
  return 'text-zinc-500';
}

export function getMethodColor(method: string) {
  switch (method.toUpperCase()) {
    case 'GET': return 'text-emerald-500';
    case 'POST': return 'text-sky-500';
    case 'PUT': return 'text-amber-500';
    case 'DELETE': return 'text-rose-500';
    case 'PATCH': return 'text-violet-500';
    default: return 'text-zinc-500';
  }
}
