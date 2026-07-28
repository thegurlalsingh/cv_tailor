import { useEffect, useState, useRef } from "react";

// This will keep the SSE‑connection logic isolated from UI;
// It also returns a restart function you can wire to a “Retry” button.

// JSDoc comment. Editors like VS Code parse it to provide: autocomplete, hover documentation, parameter hints, type checking (when checkJs is enabled)

/**
 * @param {Object} options
 * @param {string} options.url          // Full URL to the /run endpoint.
 * @param {boolean} options.autoStart   // If true (default) the connection opens on mount.
 * @returns {{logs: string[], error: Error | null, isConnected: boolean, restart: () => void}}
 */

export default function useLogStream({ url, autoStart = true, method = 'POST', headers = {}, body = {}, onEvent = null } = {}) {
    const [logs, setLogs] = useState([]);
    const [error, setErrors] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const abortControllerRef = useRef(null);

    // Helper to push a new line (with timestamp) into the state

    const pushLog = (msg) => {
        const ts = new Date().toISOString().replace('T', ' ').substring(0, 19);
        setLogs(prev => [
            ...prev,
            {
                ts,
                msg,
            }
        ]);
    };

    // Starts or restarts the SSE connection

    const start = async () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }

        abortControllerRef.current = new AbortController();
        setIsConnected(true);
        setErrors(null);
        pushLog('Starting connection to backend pipeline...');


        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', ...headers
                },
                body: JSON.stringify(body),
                signal: abortControllerRef.current.signal
            });

            if (!response.ok) {
                throw new Error(`HTTP Error! Status: ${response.status}`);
            }

            pushLog('Connection established. Waiting for agent events...');

            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';
            while (true) {
                const { done, value } = await reader.read();
                if (done) {
                    break;
                }

                buffer += decoder.decode(value, { stream: true });

                const parts = buffer.split('\n\n');
                buffer = parts.pop();

                for (const part of parts) {
                    if (part.startsWith('data:')) {
                        const jsonStr = part.replace('data: ', '');
                        try {
                            const data = JSON.parse(jsonStr);
                            if (onEvent) {
                                onEvent(data);
                            }
                            const tag = data.node ? data.node.toUpperCase() : 'INFO';
                            const updates = data.state_updates || {};
                            const summary = Object.values(updates).find((value) =>
                                value &&
                                typeof value === "object" &&
                                value.title &&
                                Array.isArray(value.bullets)
                            );
                            if (summary) {
                                setLogs(prev => [
                                    ...prev,
                                    {
                                        ts: new Date().toLocaleTimeString(),
                                        msg: tag,
                                        summary
                                    }
                                ]);
                                summary.bullets.forEach((bullet) => {
                                    pushLog(`   ✓ ${bullet}`);
                                });
                            } else {
                                pushLog(`${tag} ${data.log ?? ""}`);
                            }
                        }
                        catch (error) {
                            pushLog(`RAW  ${jsonStr}`);
                        }
                    }
                }
            }
            setIsConnected(false);
            pushLog('INFO  Pipeline finished. Connection closed.');
        }
        catch (error) {
            if (error.name === 'AbortError') {
                pushLog('Connection Aborted');
            }
            else {
                setErrors(error);
                pushLog(`Error: ${error.message}`);
                setIsConnected(false);
            }
        }
    };
    // Auto‑start on mount (if requested)

    useEffect(() => {
        if (autoStart) {
            start();
        }
        // Cleanup on unmount

        return () => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, [url, autoStart]);


    const restart = () => {
        setLogs([]);
        setErrors(null);
        start();
    };

    return { logs, error, isConnected, restart };
}
