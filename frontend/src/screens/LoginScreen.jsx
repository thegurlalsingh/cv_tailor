import React, { useState } from 'react';
import { Menu, Eye, EyeOff, ArrowRight, Loader2 } from 'lucide-react';

const API = import.meta.env.VITE_BACKEND_URL;

export default function LoginScreen({ onLoginSuccess, onGoToRegister }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);


        try {
            const res = await fetch(`${API}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'Login Failed.');
            }

            localStorage.setItem('cv_tailor_accesstoken', data.access_token);
            onLoginSuccess(data.access_token);
        }
        catch (error) {
            setError(error.message);
        }
        finally {
            setIsLoading(false);
        }
    };


    return (
        <div className='min-h-screen bg-background text-text-primary flex flex-col'>
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
                </div>
            </header>

            <main className='flex-1 flex items-center justify-center p-6'>
                <div className='w-full max-w-md'>

                    {/* Header */}
                    <div className='mb-10 text-center'>
                        <h1 className='font-mono text-3xl font-bold tracking-light mb-2'>Welcome Back!!!</h1>
                        <p className='text-text-secondary text-sm'>Sign in to access your tailoring workspace</p>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleLogin} className='flex flex-col gap-5'>

                        {/* Email */}
                        <div className='flex flex-col gap-2'>
                            <label className='font-mono text-xs text-text-secondary tracking-widest'>EMAIL</label>
                            <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} placeholder='you@example.com' required className='w-full bg-surface border border-border rounded-std px-4 py-3 font-mono text-sm text-text-primary placeholder-text-secondary focus:outline-none focus:border-primary transition-colors duration-300' />
                        </div>

                        {/* Password */}
                        <div className='flex flex-col gap-2'>
                            <label className='font-mono text-xs text-text-secondary tracking-widest'>PASSWORD</label>
                            <div className='relative'>
                                <input type={showPassword ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)} placeholder='..........' required className='w-full bg-surface border border-border rounded-std px-4 py-3 pr-12 font-mono text-sm text-text-primary placeholder-text-secondary focus:outline-none focus:border-primary transition-colors duration-300' />
                                <button type='button' onClick={() => setShowPassword(!showPassword)} className='absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-text-primary transition-colors'>
                                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                                </button>
                            </div>
                        </div>

                        {/* Error */}
                        {error && (
                            <div className='p-3 text-sm text-red-400 bg-red-900/20 border border-red-500/50 rounded font-mono'>
                                ⚠ {error}
                            </div>
                        )}

                        {/* Submit Button */}
                        <button className='mt-2 w-full bg-primary text-background font-semibold py-3 rounded-std flex items-center justify-center gap-2 hover:brightness-110 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 shadow-[0_0_20px_rgba(79,140,255,0.15)]'>
                            {isLoading ? <Loader2 size={18} className='animate-spin' /> : <ArrowRight size={18} />}
                            {isLoading ? 'Signing in....' : 'Sign in'}
                        </button>
                    </form>

                    {/* Divider */}
                    <div>
                        <div className='flex items-center gap-4 my-8'>
                            <div className='flex-1 h-px bg-border'></div>
                            <span className='text-text-secondary text-xs font-mono'>OR</span>
                            <div className='flex-1 h-px bg-border'></div>
                        </div>

                        <p className='text-center text-sm text-text-secondary'>
                            Don't have an accpunt? {' '}
                            <button onClick={onGoToRegister} className='text-primary hover:underline font-semibold transition-colors'>
                                Create one
                            </button>
                        </p>
                    </div>
                </div>
            </main>
        </div>
    )
};

