import React, { useState } from 'react';
import { UploadCloud, FileText, ArrowRight, Menu, User, Clock, ChevronRight, Loader2, CheckCircle, LogOut } from 'lucide-react';

const API = import.meta.env.VITE_BACKEND_URL;

export default function LandingScreen({ onUploadSuccess, token, onLogout }) {
    const [resumeFile, setResumeFile] = useState(null);
    const [jdText, setJdText] = useState("");
    const [isUploading, setIsUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState({ resume: null, jd: null });
    const [error, setError] = useState(null);
    const [showUserMenu, setShowUserMenu] = useState(false);


    const handleDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file) {
            setResumeFile(file);
        }
    };

    const handleInitialize = async () => {
        setIsUploading(true);
        setError(null);

        try {
            setUploadStatus({ resume: 'uploading', jd: null });
            const formData = new FormData();
            formData.append('file', resumeFile);

            const resumeRes = await fetch(`${API}/upload`, {
                method: 'POST',
                headers: { Authorization: `Bearer ${token}` },
                body: formData
            });

            if (!resumeRes.ok) {
                throw new Error('Resume upload failed.')
            }
            const resumeData = await resumeRes.json();
            setUploadStatus({ resume: 'done', jd: '' });

            setUploadStatus((s) => ({ ...s, jd: 'uploading' }));
            const jdRes = await fetch(`${API}/upload-text`, {
                method: 'POST',
                headers: { 'Content-Type': 'text/plain', Authorization: `Bearer ${token}` },
                body: jdText
            });
            if (!jdRes.ok) {
                throw new Error('Job description upload failed.')
            }
            const jdData = await jdRes.json();
            setUploadStatus({ resume: 'done', jd: 'done' });

            onUploadSuccess({
                resumeId: resumeData.resume_id,
                jdId: jdData.jd_id,
                resumeJson: resumeData.preview_of_json_output,
                jdJson: jdData.preview_of_json_output
            });
        }
        catch (err) {
            setError(err.message);
            setUploadStatus({ resume: null, jd: null });
        }
        finally {
            setIsUploading(false);
        }
    };

    const StatusIcon = ({ status }) => {
        if (status === 'uploading') {
            return <Loader2 size={16} className='animate-spin text-primary' />;
        }
        if (status === 'done') {
            return <CheckCircle size={16} className='text-green-400' />;
        }
        return null;
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

            <main className="flex flex-col items-center p-4 md:p-8">

                {/* Main Heading */}
                <div className="w-full max-w-6xl text-center mb-12 flex flex-col items-center">
                    <h1 className="font-mono text-4xl md:text-5xl font-bold tracking-tight mb-4">
                        CV Tailor
                    </h1>
                    <p className="text-text-secondary max-w-2xl text-lg">
                        Upload your base resume and the target job description. Our AI agents will mathematically analyze and rewrite your CV to bypass ATS algorithms.
                    </p>
                </div>

                {/* Grid */}
                <div className='w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 gap-8 mb-12'>

                    {/* Resume */}
                    <div className='flex flex-col gap-4'>
                        <h2 className='text-xl font-semibold tracking-tight'>
                            1. Upload Base Resume
                            <StatusIcon status={uploadStatus.resume} />
                        </h2>

                        <div
                            className='relative overflow-hidden bg-surface border border-border border-dashed rounded-card h-80 flex flex-col items-center justify-center p-8 transition-all duration-500 ease-out hover:border-primary hover:bg-surface-elevated cursor-pointer group'
                            onDragOver={(e) => e.preventDefault()}
                            onDrop={handleDrop}
                            onClick={() => document.getElementById('resume-upload').click()}
                        >
                            <input
                                id="resume-upload"
                                type="file"
                                className="hidden"
                                accept=".pdf,.docx"
                                onChange={(e) => setResumeFile(e.target.files[0])}
                            />

                            {resumeFile ? (
                                <div className='flex flex-col items-center gap-4 z-10'>
                                    <div className='p-4 bg-background rounded-full border border-border'>
                                        <FileText size={40} className="text-primary" />
                                    </div>

                                    <span className='font-mono text-sm text-text-primary text-center break-all'>
                                        {resumeFile.name}
                                    </span>

                                    <span
                                        className='text-xs text-text-secondary cursor-pointer hover:text-text-primary mt-2 transition-colors'
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setResumeFile(null);
                                        }}
                                    >
                                        Remove File
                                    </span>
                                </div>
                            ) : (
                                <div className='flex flex-col items-center gap-4 text-text-secondary text-center group-hover:text-text-primary transition-colors duration-500 z-10'>
                                    <UploadCloud size={48} strokeWidth={1.5} />
                                    <p>
                                        Drag and drop your PDF/DOCX here
                                        <br />
                                        <span className="opacity-70 text-sm">
                                            or click to browse
                                        </span>
                                    </p>
                                </div>
                            )}

                            <div className="absolute bottom-0 left-0 h-1 bg-primary w-0 group-hover:w-full transition-all duration-700 ease-in-out"></div>
                        </div>
                    </div>

                    {/* JD */}
                    <div className='flex flex-col gap-4'>
                        <h2 className='text-xl font-semibold tracking-tight'>
                            2. Target Job Description
                            <StatusIcon status={uploadStatus.jd} />
                        </h2>

                        <div className="relative h-80 group overflow-hidden rounded-card">

                            <textarea
                                className='absolute inset-0 w-full h-full bg-surface border hover:border-dashed hover:border-primary border-border rounded-card p-6 text-text-primary placeholder-text-secondary transition-all duration-500 ease-out resize-none font-mono text-sm leading-relaxed z-10 bg-transparent'
                                placeholder='Paste the target job description here....'
                                value={jdText}
                                onChange={(e) => setJdText(e.target.value)}
                            />

                            <div className="absolute bottom-0 left-0 h-1 bg-primary w-0 group-hover:w-full transition-all duration-700 ease-in-out z-20 pointer-events-none"></div>

                        </div>
                    </div>

                </div>

                {error && (
                    <div className='mb-6 p-3 text-sm text-red-400 bg-red-900/20 border border-red-500 rounded font-mono'>
                        ⚠ {error}
                    </div>
                )}

                {/* Button */}
                <button
                    className='mb-16 bg-primary text-background font-semibold px-8 py-4 rounded-std hover:brightness-110 hover:-translate-y-1 active:translate-y-0 transition-all duration-300 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 shadow-[0_0_20px_rgba(79,140,255,0.15)]'
                    disabled={!resumeFile || !jdText}
                    onClick={handleInitialize}
                >
                    {isUploading ? <Loader2 size={18} className='animate-spin' /> : <ArrowRight size={20} strokeWidth={2.5} />}
                    {isUploading ? 'Uploading...' : 'Initialize Tailoring Engine'}
                </button>

                {/* Recent */}
                <div className="w-full max-w-6xl mt-8 mb-16">
                    <h3 className="text-lg font-semibold tracking-tight mb-4 flex items-center gap-2">
                        <Clock size={18} className="text-text-secondary" />
                        Recent Tailorings
                    </h3>

                    <div className="flex flex-col gap-3">

                        <div className="bg-surface border border-border rounded-std p-4 flex justify-between items-center hover:bg-surface-elevated hover:border-primary transition-colors cursor-pointer group">
                            <div className="flex flex-col">
                                <span className="font-semibold">
                                    Frontend Engineer @ Stripe
                                </span>

                                <span className="text-xs text-text-secondary font-mono mt-1">
                                    tailored_resume_stripe.pdf
                                </span>
                            </div>

                            <div className="flex items-center gap-4">
                                <span className="text-xs text-text-secondary hidden md:block">
                                    2 hours ago
                                </span>

                                <ChevronRight
                                    size={18}
                                    className="text-text-secondary group-hover:text-primary transition-colors"
                                />
                            </div>
                        </div>

                        <div className="bg-surface border border-border rounded-std p-4 flex justify-between items-center hover:bg-surface-elevated hover:border-primary transition-colors cursor-pointer group">
                            <div className="flex flex-col">
                                <span className="font-semibold">
                                    Fullstack Developer @ Vercel
                                </span>

                                <span className="text-xs text-text-secondary font-mono mt-1">
                                    tailored_resume_vercel.pdf
                                </span>
                            </div>

                            <div className="flex items-center gap-4">
                                <span className="text-xs text-text-secondary hidden md:block">
                                    Yesterday
                                </span>

                                <ChevronRight
                                    size={18}
                                    className="text-text-secondary group-hover:text-primary transition-colors"
                                />
                            </div>
                        </div>

                    </div>
                </div>

            </main>

        </div>
    );
}