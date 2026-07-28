import React, { useState } from 'react';
import { Download, CheckCircle, Menu, User, LogOut, ArrowLeft, Check } from 'lucide-react';

export default function ResultScreen({ downloadUrl, atsScore, onGoBack, onLogout }) {
    const [showUserMenu, setShowUserMenu] = useState(false);

    const getScoreColor = (score) => {
        if (score >= 80) {
            return 'text-green-400';
        }
        if (score >= 60) {
            return 'text-yellow-400';
        }
        return 'text-red-400';
    };

    const getBarColor = (score) => {
        if (score >= 80) {
            return 'bg-green-500';
        }
        if (score >= 60) {
            return 'bg-yellow-500';
        }
        return 'bg-red-500';
    };

    return (
        <div className='min-h-screen bg-background text-text-primary flex flex-col'>
            {/* Navbar */}
            <header className="w-full h-16 bg-[#0d0d0d] border-b border-white/10">
                <div className="w-full h-full px-6 flex items-center justify-between">


                    <div className='flex items-center gap-6'>
                        <button className="w-10 h-10 flex items-center justify-center hover:bg-white/5 transition">
                            <Menu size={20} />
                        </button>

                        <p className='font-mono text-text-primary'>RESUME.OS</p>
                    </div>

                    {/* <div className="text-xl font-bold tracking-tight">
                                    CV Tailor
                                </div> */}

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

            <main className='flex-1 flex items-center justify-center p-6'>
                <div className='w-full max-w-lg flex flex-col items-center'>

                    <div className="w-20 h-20 rounded-full bg-green-500/10 border border-green-500/30 flex items-center justify-center mb-8">
                        <CheckCircle size={40} className='text-green-400' />
                    </div>

                    <h1 className='font-mono text-3xl font-bold tracking-tight mb-2 text-center'>Tailoring Complete!!</h1>
                    <p className='text-text-secondary text-sm text-center mb-10'>Your resume has been optimized and is ready for download.</p>
                    <div className='w-full bg-surface border border-border rounded-card p-8 mb-8'>
                        <div className='flex justify-between items-end mb-4'>
                            <span className='font-mono text-xs text-text-secondary tracking-widest'>FINAL ATS MATCH SCORE</span>
                            <span className={`text-5xl font-bold font-mono ${getScoreColor(atsScore || 0)}`}>{atsScore || '-'} %</span>
                        </div>
                        <div className='w-full bg-[#222] h-3 rounded-full overflow-hidden'>
                            <div className={`h-full rounded-full transition-all duration-1000 ease-out ${getBarColor(atsScore || 0)}`} style={{ width: `${atsScore || 0}%` }}></div>

                        </div>

                        <p className="text-text-secondary text-xs font-mono mt-3">
                            {atsScore >= 80 ? 'Great score — your resume is highly ATS-compatible.' :
                                atsScore >= 60 ? 'Decent score — some room for improvement.' :
                                    'Low score — consider revising further.'}
                        </p>
                    </div>

                    <a href={downloadUrl} target='_blank' rel='noopener noreferrer' className="w-full bg-primary text-background font-semibold py-4 rounded-std flex items-center justify-center gap-3 hover:brightness-110 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-300 shadow-[0_0_25px_rgba(79,140,255,0.2)] text-lg">
                        <Download size={20} /> Download Tailored Resume
                    </a>

                    <button onClick={onGoBack} className="mt-6 text-text-secondary text-sm font-mono flex items-center gap-2 hover:text-text-primary transition-colors">
                        <ArrowLeft size={14} /> Tailor another resume
                    </button>
                </div>
            </main>

        </div>
    )
}