import React from "react";
import { Download, Maximize2 } from "lucide-react";

export default function TerminalConsole({ logs }) {
    return (
        <div className="flex flex-col h-full bg-[#0E0E0E] border border-border rounded-lg overflow-hidden font-mono text-[13px]">

            {/* Terminal Window Header */}

            <div className="flex items-center justify-between px-4 py-2 border-b border-border/50 bg-[#141414]">

                {/* Mac OS Window Controls */}

                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#FF5F56]"></div>
                    <div className="w-3 h-3 rounded-full bg-[#FFBD2E]"></div>
                    <div className="w-3 h-3 rounded-full bg-[#27C93F]"></div>
                </div>
                <div className="text-text-secondary text-xs tracking-wider opacity-80">
                    pipeline-process-stdout-tail -f
                </div>

                {/* Actions */}

                <div className="flex items-center gap-3 text-text-secondary">
                    <Download size={14} className="hover:text-text-primary cursor-pointer transition-colors" />
                    <Maximize2 size={14} className="hover:text-text-primary cursor-pointer transition-colors" />
                </div>
            </div>

            <div className="flex-1 p-4 overflow-y-auto leading-relaxed">
                {logs.length === 0 && (
                    <div className="text-text-secondary">Waiting for pipeline to start</div>
                )}

                {logs.map((log, index) => {
                    const isInfo = log.msg?.includes('INFO');
                    const isRunning = log.msg?.includes('RUNNING');
                    const isSync = log.msg?.includes('SYNC');
                    const isWarning = log.msg?.includes('WARNING');

                    return (
                        <div key={index} className="mb-3">
                            {/* Log Line */}
                            <div className="flex gap-2 flex-wrap">
                                <span className="text-text-secondary shrink-0">[{log.ts}]</span>
                                {isInfo && <span className="text-primary font-bold shrink-0">INFO</span>}
                                {isRunning && <span className="text-yellow-400 font-bold shrink-0">RUNNING</span>}
                                {isSync && <span className="text-green-400 font-bold shrink-0">SYNC</span>}
                                {isWarning && <span className="text-red-400 font-bold shrink-0">WARNING</span>}
                                <span className="text-text-primary break-words">{log.msg?.replace(/INFO|RUNNING|SYNC|WARNING/g, '').trim()}</span>
                            </div>

                            {/* Optional UI Summary Card */}
                            {log.summary && (
                                <div className="mt-2 ml-4 border-l-2 border-primary/40 pl-3 py-1">
                                    <p className="text-primary text-xs font-bold tracking-wider mb-1">{log.summary.title}</p>
                                    {log.summary.bullets?.map((b, i) => (
                                        <p key={i} className="text-text-secondary text-xs">→ {b}</p>
                                    ))}
                                </div>
                            )}
                        </div>
                    );
                })}


                <div className="mt-2 text-primary animate-pulse">_</div>
            </div>
        </div>
    )
}