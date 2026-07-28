import { useState, useEffect } from 'react';
import LoginScreen from './screens/LoginScreen';
import RegisterScreen from './screens/RegisterScreen';
import LandingScreen from './screens/LandingScreen';
import WorkspaceScreen from './screens/WorkspaceScreen';
import ResultsScreen from './screens/ResultsScreen';

function App() {
  const [screen, setScreen] = useState(() => {
    return localStorage.getItem('cv_tailor_accesstoken') ? 'landing' : 'login';
  });
  const [token, setToken] = useState(() => localStorage.getItem('cv_tailor_accesstoken'));
  const [session, setSession] = useState({
    resumeId: null,
    jdId: null,
    resumeJson: null,
    jdJson: null
  });
  const [results, setResults] = useState({ downloadUrl: null, atsScore: null });

  const handleUploadSuccess = (sessionData) => {
    setSession(sessionData);
    setScreen('workspace');
  }

  const handleLoginSuccess = (newToken) => {
    setToken(newToken);
    setScreen('landing');
  }

  const handleRegister = () => {
    setScreen('login');
  }

  const handleLogout = () => {
    localStorage.removeItem('cv_tailor_accesstoken');
    setToken(null);
    setScreen('login');
  }

  const handleViewResults = ({ downloadUrl, atsScore }) => {
    setResults({ downloadUrl, atsScore });
    setScreen('results');
  }

  return (
    <>
      {screen === 'login' && (
        <LoginScreen onLoginSuccess={handleLoginSuccess} onGoToRegister={() => setScreen('register')} />
      )}

      {screen === 'register' && (
        <RegisterScreen onRegisterSuccess={handleRegister} onGoToLogin={() => setScreen('login')} />
      )}

      {screen === 'landing' && (
        <LandingScreen onUploadSuccess={handleUploadSuccess} token={token} onLogout={handleLogout} />
      )}

      {screen === 'workspace' && (
        <WorkspaceScreen session={session} onViewResults={handleViewResults} onLogout={handleLogout} token={token} />
      )}

      {screen === 'results' && (
        <ResultsScreen
          downloadUrl={results.downloadUrl}
          atsScore={results.atsScore}
          onGoBack={() => setScreen('landing')}
          onLogout={handleLogout}
        />
      )}
    </>
  )
}

export default App;


