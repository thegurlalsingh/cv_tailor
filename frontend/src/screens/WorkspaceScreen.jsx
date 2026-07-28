import { useState } from 'react';
import React from 'react';
import TerminalConsole from '../components/TerminalConsole';
import useLogStream from '../hooks/useLogStream.js';
import { CheckCircle, ExternalLink, ArrowRight, Menu, User, LogOut } from 'lucide-react';

// const sampleLogs = [
//     "INFO    Starting pipeline...",
//     "RUNNING    Parsing resume...",
//     "INFO    Resume parsed successfully.",
//     "RUNNING    Generating keyword suggestions...",
//     "INFO    Keyword extraction complete.",
//     "SYNC    Syncing with ATS scoring model...",
//     "INFO    Pipeline finished – ready for preview."
// ];

const API = import.meta.env.VITE_BACKEND_URL;

export default function WorkspaceScreen({ session, token, onLogout, onViewResults }) {
    const [downloadUrl, setDownloadUrl] = useState(null);
    const [atsScore, setAtsScore] = useState(null);
    const [showUserMenu, setShowUserMenu] = useState(false);
    const onFinalEvent = (event) => {
        if (event.download_url) {
            setDownloadUrl(event.download_url);
        }


        const updates = event.state_updates || {};
        if (updates.ats_report && updates.ats_report.overall_score) {
            setAtsScore(updates.ats_report.overall_score);
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
        <div className="min-h-screen bg-background text-text-primary flex flex-col p-4 md:p-8">

            {/* Navbar */}

            <header className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold">Tailoring Workspace</h1>
                <div className='flex items-center gap-3'>
                    {isConnected && (
                        <span className='text-xs font-mono text-primary flex items-center gap-1'>
                            <span className='w-2 h-2 rounded-full bg-primary animate-pulse'></span>
                            Agents Running
                        </span>
                    )}
                    <button className='flex items-center gap-2 px-4 py-2 rounded-std bg-green-600 text-white font-semibold text-sm hover:brightness-110 transition-all disabled:opacity-30 disabled:cursor-not-allowed'
                        onClick={() => onViewResults(downloadUrl, atsScore)}
                        disabled={!downloadUrl}>
                        <CheckCircle size={16} />
                        View Results
                        <ExternalLink size={14} />
                    </button>

                    <div className='relative'>
                        <button onClick={() => setShowUserMenu(!showUserMenu)} className='w-10 h-10 rounded-full bordder border-border flex items-center justify-center hover:bg-white/5 transition'>
                            <User size={18} className='text-text-secondary' />
                        </button>

                        {showUserMenu && (
                            <div className='absolute right-0 top-12 bg-surface border border-border rounded-std shadow-lg z-50 overflow-hidden min-w-[160px]'>
                                <button onClick={() => { setShowUserMenu(false); onLogout(); }} className='w-full px-4 py-3 text-left text-sm font-mono text-red-400 hover:bg-red-900/20 transition-colors flex items-center gap-2'>
                                    <LogOut size={14} /> Logout
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </header>

            <div className='flex-1 flex flex-col p-4 md:p-8'>
                {error && (
                    <div className='mb-4 p-3 text-sm text-red-400 bg-red-900/20 border border-red-500 rounded font-mono'>{error.message}</div>
                )}
                {/* The actual terminal component */}
                <TerminalConsole logs={logs} />
            </div>


        </div>
    )
}