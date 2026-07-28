import { useState } from 'react';
import React from 'react';
import TerminalConsole from '../components/TerminalConsole';
import useLogStream from '../hooks/useLogStream.js';
import { CheckCircle, ArrowRight, Menu, User, LogOut } from 'lucide-react';

const API = import.meta.env.VITE_BACKEND_URL;

export default function WorkspaceScreen({ session, token, onViewResults, onLogout }) {
    const [downloadUrl, setDownloadUrl] = useState(null);
    const [atsScore, setAtsScore] = useState(null);
    const [showUserMenu, setShowUserMenu] = useState(false);

    const onFinalEvent = (event) => {
        if (event.download_url) {
            setDownloadUrl(event.download_url);
        }
        const updates = event.state_updates || {};
        if (updates.ats_score !== undefined && updates.ats_score !== null) {
            setAtsScore(updates.ats_score);
        }
    };

    const { logs, error, isConnected } = useLogStream({
        url: `${API}/run`,
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: {
            original_resume_json: session.resumeJson,
            job_description_json: session.jdJson,
            resume_id: session.resumeId,
            jd_id: session.jdId,
        },
        onEvent: onFinalEvent,
    });

    return (
        <div className="min-h-screen bg-background text-text-primary flex flex-col">
            {/* Navbar */}
            <header className="w-full h-16 bg-[#0d0d0d] border-b border-white/10">
                <div className="w-full h-full px-6 flex items-center justify-between">
                    <div className="flex items-center gap-6">
                        <button className="w-10 h-10 flex items-center justify-center hover:bg-white/5 transition">
                            <Menu size={20} />
                        </button>
                        <p className="font-mono text-text-primary">RESUME.OS</p>
                    </div>

                    <div className="flex items-center gap-4">
                        {/* Live status */}
                        {isConnected && (
                            <span className="text-xs font-mono text-primary flex items-center gap-1">
                                <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
                                Agents Running
                            </span>
                        )}

                        {/* View Results Button */}
                        <button
                            onClick={() => onViewResults({ downloadUrl, atsScore })}
                            disabled={!downloadUrl}
                            className="flex items-center gap-2 px-4 py-2 rounded-std bg-green-600 text-white font-semibold text-sm hover:brightness-110 transition-all disabled:opacity-30 disabled:cursor-not-allowed"
                        >
                            <CheckCircle size={16} />
                            View Results
                            <ArrowRight size={14} />
                        </button>

                        {/* User Menu */}
                        <div className="relative">
                            <button
                                onClick={() => setShowUserMenu(!showUserMenu)}
                                className="w-10 h-10 rounded-full border border-border flex items-center justify-center hover:bg-white/5 transition"
                            >
                                <User size={18} className="text-text-secondary" />
                            </button>

                            {showUserMenu && (
                                <div className="absolute right-0 top-12 bg-surface border border-border rounded-std shadow-lg z-50 overflow-hidden min-w-[160px]">
                                    <button
                                        onClick={() => {
                                            setShowUserMenu(false);
                                            onLogout();
                                        }}
                                        className="w-full px-4 py-3 text-left text-sm font-mono text-red-400 hover:bg-red-900/20 transition-colors flex items-center gap-2"
                                    >
                                        <LogOut size={14} />
                                        Logout
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </header>

            {/* Content */}
            <div className="flex-1 flex flex-col p-4 md:p-8">
                {error && (
                    <div className="mb-4 p-3 text-sm text-red-400 bg-red-900/20 border border-red-500 rounded font-mono">
                        {error.message}
                    </div>
                )}
                <TerminalConsole logs={logs} />
            </div>
        </div>
    );
}
