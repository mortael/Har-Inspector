import { Search, Filter, Trash2, Download, ChevronRight, ChevronDown, Clock, Globe, Shield, Database, Edit2, Save, X, Plus } from 'lucide-react';
import React, { useState, useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HarEntry, HarData } from '../types';
import { cn, formatBytes, getStatusColor, getMethodColor } from '../utils';
import { format } from 'date-fns';

interface HarViewerProps {
  data: HarData;
  onUpdate: (data: HarData) => void;
  onReset: () => void;
}

export function HarViewer({ data, onUpdate, onReset }: HarViewerProps) {
  const [search, setSearch] = useState('');
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [filterMethod, setFilterMethod] = useState<string>('ALL');
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState<HarEntry | null>(null);

  const entries = useMemo(() => {
    return data.log.entries.map((e, i) => ({ ...e, _id: e._id || `entry-${i}` }));
  }, [data]);

  const filteredEntries = useMemo(() => {
    return entries.filter(entry => {
      const matchesSearch = entry.request.url.toLowerCase().includes(search.toLowerCase());
      const matchesMethod = filterMethod === 'ALL' || entry.request.method === filterMethod;
      return matchesSearch && matchesMethod;
    });
  }, [entries, search, filterMethod]);

  const selectedEntry = useMemo(() => {
    return entries.find(e => e._id === selectedId);
  }, [entries, selectedId]);

  useEffect(() => {
    if (selectedEntry && isEditing) {
      setEditForm(JSON.parse(JSON.stringify(selectedEntry)));
    } else {
      setEditForm(null);
    }
  }, [selectedEntry, isEditing]);

  const removeEntry = (id: string) => {
    const newData = {
      ...data,
      log: {
        ...data.log,
        entries: data.log.entries.filter((_, i) => entries[i]._id !== id)
      }
    };
    onUpdate(newData);
    if (selectedId === id) setSelectedId(null);
  };

  const saveEntry = () => {
    if (!editForm || !selectedId) return;
    
    const entryIndex = entries.findIndex(e => e._id === selectedId);
    if (entryIndex === -1) return;

    const newEntries = [...data.log.entries];
    // Remove internal _id before saving back to data
    const { _id, ...cleanEntry } = editForm as any;
    newEntries[entryIndex] = cleanEntry;

    onUpdate({
      ...data,
      log: {
        ...data.log,
        entries: newEntries
      }
    });
    setIsEditing(false);
  };

  const exportAsJson = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'modified_capture.har';
    a.click();
  };

  const exportAsCsv = () => {
    const headers = ['Method', 'URL', 'Status', 'Size', 'Time (ms)'];
    const rows = filteredEntries.map(e => [
      e.request.method,
      e.request.url,
      e.response.status,
      e.response.content.size,
      e.time
    ]);
    const csvContent = [headers, ...rows].map(r => r.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'network_log.csv';
    a.click();
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center justify-between p-4 bg-zinc-900/50 border-b border-zinc-800 gap-4">
        <div className="flex items-center gap-4 flex-1">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
            <input
              type="text"
              placeholder="Filter by URL..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-emerald-500/50 transition-colors"
            />
          </div>
          <select
            value={filterMethod}
            onChange={(e) => setFilterMethod(e.target.value)}
            className="bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500/50"
          >
            <option value="ALL">All Methods</option>
            <option value="GET">GET</option>
            <option value="POST">POST</option>
            <option value="PUT">PUT</option>
            <option value="DELETE">DELETE</option>
            <option value="PATCH">PATCH</option>
          </select>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={exportAsCsv}
            className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 rounded-lg transition-colors"
          >
            <Database className="w-4 h-4" />
            Export CSV
          </button>
          <button
            onClick={exportAsJson}
            className="flex items-center gap-2 px-3 py-2 text-sm font-medium bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20 rounded-lg transition-colors border border-emerald-500/20"
          >
            <Download className="w-4 h-4" />
            Save HAR
          </button>
          <button
            onClick={onReset}
            className="p-2 text-zinc-500 hover:text-rose-500 hover:bg-rose-500/10 rounded-lg transition-colors"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Entry List */}
        <div className={cn(
          "flex-1 overflow-y-auto custom-scrollbar border-r border-zinc-800 bg-zinc-950",
          selectedId ? "hidden lg:block lg:max-w-md xl:max-w-xl" : "block"
        )}>
          <table className="w-full text-left text-sm border-collapse">
            <thead className="sticky top-0 bg-zinc-900 z-10">
              <tr className="border-b border-zinc-800">
                <th className="px-4 py-3 font-medium text-zinc-500">Status</th>
                <th className="px-4 py-3 font-medium text-zinc-500">Method</th>
                <th className="px-4 py-3 font-medium text-zinc-500">URL</th>
                <th className="px-4 py-3 font-medium text-zinc-500 text-right">Size</th>
                <th className="px-4 py-3 font-medium text-zinc-500 text-right">Time</th>
              </tr>
            </thead>
            <tbody>
              {filteredEntries.map((entry) => (
                <tr
                  key={entry._id}
                  onClick={() => setSelectedId(entry._id!)}
                  className={cn(
                    "group cursor-pointer border-b border-zinc-900/50 transition-colors",
                    selectedId === entry._id ? "bg-emerald-500/10" : "hover:bg-zinc-900"
                  )}
                >
                  <td className={cn("px-4 py-3 font-mono font-medium", getStatusColor(entry.response.status))}>
                    {entry.response.status}
                  </td>
                  <td className={cn("px-4 py-3 font-bold", getMethodColor(entry.request.method))}>
                    {entry.request.method}
                  </td>
                  <td className="px-4 py-3 max-w-xs truncate text-zinc-300">
                    {entry.request.url}
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-500 font-mono">
                    {formatBytes(entry.response.content.size)}
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-500 font-mono">
                    {Math.round(entry.time)}ms
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredEntries.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20 text-zinc-500">
              <Search className="w-12 h-12 mb-4 opacity-20" />
              <p>No entries matching your search</p>
            </div>
          )}
        </div>

        {/* Details Panel */}
        <AnimatePresence mode="wait">
          {selectedEntry && (
            <motion.div
              initial={{ x: 20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 20, opacity: 0 }}
              className="flex-1 flex flex-col bg-zinc-950 overflow-hidden"
            >
              <div className="flex items-center justify-between p-4 border-b border-zinc-800 bg-zinc-900/30">
                <div className="flex items-center gap-4 overflow-hidden">
                  <button
                    onClick={() => {
                      setSelectedId(null);
                      setIsEditing(false);
                    }}
                    className="lg:hidden p-2 text-zinc-500 hover:text-white"
                  >
                    <ChevronRight className="w-5 h-5 rotate-180" />
                  </button>
                  <div className="flex flex-col overflow-hidden">
                    <div className="flex items-center gap-2">
                      <span className={cn("font-bold", getMethodColor(selectedEntry.request.method))}>
                        {selectedEntry.request.method}
                      </span>
                      <span className="text-zinc-500">/</span>
                      <span className={cn("font-mono", getStatusColor(selectedEntry.response.status))}>
                        {selectedEntry.response.status}
                      </span>
                    </div>
                    <span className="text-xs text-zinc-500 truncate font-mono">
                      {selectedEntry.request.url}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {!isEditing ? (
                    <button
                      onClick={() => setIsEditing(true)}
                      className="p-2 text-zinc-500 hover:text-emerald-500 hover:bg-emerald-500/10 rounded-lg transition-colors"
                      title="Edit entry"
                    >
                      <Edit2 className="w-4 h-4" />
                    </button>
                  ) : (
                    <div className="flex items-center gap-2">
                      <button
                        onClick={saveEntry}
                        className="p-2 text-emerald-500 hover:bg-emerald-500/10 rounded-lg transition-colors"
                        title="Save changes"
                      >
                        <Save className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => setIsEditing(false)}
                        className="p-2 text-rose-500 hover:bg-rose-500/10 rounded-lg transition-colors"
                        title="Cancel"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                  <button
                    onClick={() => removeEntry(selectedEntry._id!)}
                    className="p-2 text-zinc-500 hover:text-rose-500 hover:bg-rose-500/10 rounded-lg transition-colors"
                    title="Remove from log"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div className="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-8">
                {isEditing && editForm ? (
                  <div className="space-y-6">
                    <Section title="Basic Inforamtion">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <label className="text-xs text-zinc-500 uppercase font-bold">URL</label>
                          <input
                            type="text"
                            value={editForm.request.url}
                            onChange={(e) => setEditForm({
                              ...editForm,
                              request: { ...editForm.request, url: e.target.value }
                            })}
                            className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500/50 transition-colors font-mono"
                          />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                          <div className="space-y-2">
                            <label className="text-xs text-zinc-500 uppercase font-bold">Method</label>
                            <select
                              value={editForm.request.method}
                              onChange={(e) => setEditForm({
                                ...editForm,
                                request: { ...editForm.request, method: e.target.value }
                              })}
                              className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500/50 transition-colors"
                            >
                              {['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'].map(m => (
                                <option key={m} value={m}>{m}</option>
                              ))}
                            </select>
                          </div>
                          <div className="space-y-2">
                            <label className="text-xs text-zinc-500 uppercase font-bold">Status</label>
                            <input
                              type="number"
                              value={editForm.response.status}
                              onChange={(e) => setEditForm({
                                ...editForm,
                                response: { ...editForm.response, status: parseInt(e.target.value) || 0 }
                              })}
                              className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500/50 transition-colors font-mono"
                            />
                          </div>
                        </div>
                      </div>
                    </Section>

                    <Section title="Edit Request Headers">
                      <div className="space-y-2">
                        {editForm.request.headers.map((h, i) => (
                          <div key={i} className="flex gap-2 items-center">
                            <input
                              type="text"
                              value={h.name}
                              onChange={(e) => {
                                const newHeaders = [...editForm.request.headers];
                                newHeaders[i].name = e.target.value;
                                setEditForm({ ...editForm, request: { ...editForm.request, headers: newHeaders } });
                              }}
                              className="flex-1 bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-emerald-500/50 font-mono"
                              placeholder="Name"
                            />
                            <input
                              type="text"
                              value={h.value}
                              onChange={(e) => {
                                const newHeaders = [...editForm.request.headers];
                                newHeaders[i].value = e.target.value;
                                setEditForm({ ...editForm, request: { ...editForm.request, headers: newHeaders } });
                              }}
                              className="flex-[2] bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-emerald-500/50 font-mono"
                              placeholder="Value"
                            />
                            <button
                              onClick={() => {
                                const newHeaders = editForm.request.headers.filter((_, idx) => idx !== i);
                                setEditForm({ ...editForm, request: { ...editForm.request, headers: newHeaders } });
                              }}
                              className="p-1.5 text-zinc-500 hover:text-rose-500 transition-colors"
                            >
                              <X className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        ))}
                        <button
                          onClick={() => {
                            setEditForm({
                              ...editForm,
                              request: {
                                ...editForm.request,
                                headers: [...editForm.request.headers, { name: '', value: '' }]
                              }
                            });
                          }}
                          className="flex items-center gap-2 text-xs text-emerald-500 hover:text-emerald-400 transition-colors mt-2"
                        >
                          <Plus className="w-3.5 h-3.5" /> Add Header
                        </button>
                      </div>
                    </Section>

                    <Section title="Edit Response Headers">
                      <div className="space-y-2">
                        {editForm.response.headers.map((h, i) => (
                          <div key={i} className="flex gap-2 items-center">
                            <input
                              type="text"
                              value={h.name}
                              onChange={(e) => {
                                const newHeaders = [...editForm.response.headers];
                                newHeaders[i].name = e.target.value;
                                setEditForm({ ...editForm, response: { ...editForm.response, headers: newHeaders } });
                              }}
                              className="flex-1 bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-emerald-500/50 font-mono"
                              placeholder="Name"
                            />
                            <input
                              type="text"
                              value={h.value}
                              onChange={(e) => {
                                const newHeaders = [...editForm.response.headers];
                                newHeaders[i].value = e.target.value;
                                setEditForm({ ...editForm, response: { ...editForm.response, headers: newHeaders } });
                              }}
                              className="flex-[2] bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-emerald-500/50 font-mono"
                              placeholder="Value"
                            />
                            <button
                              onClick={() => {
                                const newHeaders = editForm.response.headers.filter((_, idx) => idx !== i);
                                setEditForm({ ...editForm, response: { ...editForm.response, headers: newHeaders } });
                              }}
                              className="p-1.5 text-zinc-500 hover:text-rose-500 transition-colors"
                            >
                              <X className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        ))}
                        <button
                          onClick={() => {
                            setEditForm({
                              ...editForm,
                              response: {
                                ...editForm.response,
                                headers: [...editForm.response.headers, { name: '', value: '' }]
                              }
                            });
                          }}
                          className="flex items-center gap-2 text-xs text-emerald-500 hover:text-emerald-400 transition-colors mt-2"
                        >
                          <Plus className="w-3.5 h-3.5" /> Add Header
                        </button>
                      </div>
                    </Section>

                    {editForm.request.postData && (
                      <Section title="Edit Request Body">
                        <textarea
                          value={editForm.request.postData.text || ''}
                          onChange={(e) => setEditForm({
                            ...editForm,
                            request: {
                              ...editForm.request,
                              postData: { ...editForm.request.postData!, text: e.target.value }
                            }
                          })}
                          rows={6}
                          className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-2 text-xs focus:outline-none focus:border-emerald-500/50 transition-colors font-mono custom-scrollbar"
                          placeholder="Request body text..."
                        />
                      </Section>
                    )}

                    <Section title="Edit Response Content">
                      <textarea
                        value={editForm.response.content.text || ''}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          response: {
                            ...editForm.response,
                            content: { ...editForm.response.content, text: e.target.value }
                          }
                        })}
                        rows={8}
                        className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-2 text-xs focus:outline-none focus:border-emerald-500/50 transition-colors font-mono custom-scrollbar"
                        placeholder="Response body text..."
                      />
                    </Section>
                  </div>
                ) : (
                  <>
                    {/* Summary Info */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="p-3 rounded-xl bg-zinc-900/50 border border-zinc-800">
                        <div className="flex items-center gap-2 text-xs text-zinc-500 mb-1">
                          <Clock className="w-3 h-3" />
                          Started
                        </div>
                        <div className="text-sm font-mono">
                          {format(new Date(selectedEntry.startedDateTime), 'HH:mm:ss.SSS')}
                        </div>
                      </div>
                      <div className="p-3 rounded-xl bg-zinc-900/50 border border-zinc-800">
                        <div className="flex items-center gap-2 text-xs text-zinc-500 mb-1">
                          <Globe className="w-3 h-3" />
                          IP Address
                        </div>
                        <div className="text-sm font-mono">
                          {selectedEntry.serverIPAddress || 'Unknown'}
                        </div>
                      </div>
                      <div className="p-3 rounded-xl bg-zinc-900/50 border border-zinc-800">
                        <div className="flex items-center gap-2 text-xs text-zinc-500 mb-1">
                          <Shield className="w-3 h-3" />
                          Protocol
                        </div>
                        <div className="text-sm font-mono">
                          {selectedEntry.request.httpVersion}
                        </div>
                      </div>
                      <div className="p-3 rounded-xl bg-zinc-900/50 border border-zinc-800">
                        <div className="flex items-center gap-2 text-xs text-zinc-500 mb-1">
                          <Database className="w-3 h-3" />
                          Content Type
                        </div>
                        <div className="text-sm font-mono truncate">
                          {selectedEntry.response.content.mimeType}
                        </div>
                      </div>
                    </div>

                    {/* Headers Section */}
                    <Section title="Request Headers">
                      <div className="space-y-1">
                        {selectedEntry.request.headers.map((h: { name: string; value: string }, i: number) => (
                          <HeaderRow key={i} name={h.name} value={h.value} />
                        ))}
                      </div>
                    </Section>

                    <Section title="Response Headers">
                      <div className="space-y-1">
                        {selectedEntry.response.headers.map((h: { name: string; value: string }, i: number) => (
                          <HeaderRow key={i} name={h.name} value={h.value} />
                        ))}
                      </div>
                    </Section>

                    {/* Body Section */}
                    {selectedEntry.request.postData && (
                      <Section title="Request Body">
                        <pre className="p-4 rounded-xl bg-zinc-900 border border-zinc-800 text-xs font-mono overflow-x-auto custom-scrollbar text-zinc-400">
                          {selectedEntry.request.postData.text || 'No text content'}
                        </pre>
                      </Section>
                    )}

                    {selectedEntry.response.content.text && (
                      <Section title="Response Content">
                        <pre className="p-4 rounded-xl bg-zinc-900 border border-zinc-800 text-xs font-mono overflow-x-auto custom-scrollbar text-zinc-400">
                          {selectedEntry.response.content.text}
                        </pre>
                      </Section>
                    )}

                    {/* Timings */}
                    <Section title="Timing Breakdown">
                      <div className="space-y-3">
                        <TimingBar label="DNS" value={selectedEntry.timings.dns} color="bg-sky-500" />
                        <TimingBar label="Connect" value={selectedEntry.timings.connect} color="bg-amber-500" />
                        <TimingBar label="Wait" value={selectedEntry.timings.wait} color="bg-emerald-500" />
                        <TimingBar label="Receive" value={selectedEntry.timings.receive} color="bg-violet-500" />
                      </div>
                    </Section>
                  </>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

const Section: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => {
  const [isOpen, setIsOpen] = useState(true);
  return (
    <div className="space-y-3">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-zinc-500 hover:text-zinc-300 transition-colors"
      >
        {isOpen ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
        {title}
      </button>
      {isOpen && <div className="pl-5">{children}</div>}
    </div>
  );
};

const HeaderRow: React.FC<{ name: string; value: string }> = ({ name, value }) => {
  return (
    <div className="flex gap-4 py-1 text-xs group">
      <div className="w-32 shrink-0 font-medium text-zinc-500 break-all">{name}:</div>
      <div className="text-zinc-300 break-all font-mono">{value}</div>
    </div>
  );
};

const TimingBar: React.FC<{ label: string; value: number; color: string }> = ({ label, value, color }) => {
  if (value < 0) return null;
  return (
    <div className="flex items-center gap-4 text-xs">
      <div className="w-16 text-zinc-500">{label}</div>
      <div className="flex-1 h-1.5 bg-zinc-900 rounded-full overflow-hidden">
        <div className={cn("h-full rounded-full", color)} style={{ width: `${Math.min(100, (value / 1000) * 100)}%` }} />
      </div>
      <div className="w-12 text-right text-zinc-400 font-mono">{Math.round(value)}ms</div>
    </div>
  );
};
