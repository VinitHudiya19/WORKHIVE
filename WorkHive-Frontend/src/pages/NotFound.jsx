import { useNavigate } from 'react-router-dom'
import { AlertCircle, ArrowLeft } from 'lucide-react'

export default function NotFound() {
  const navigate = useNavigate()

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      background: 'var(--surface-bg)',
      padding: 'var(--space-6)',
      textAlign: 'center'
    }}>
      <div style={{
        background: 'var(--surface-card)',
        padding: '3rem',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-md)',
        maxWidth: '480px',
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '1.5rem'
      }}>
        <div style={{
          width: '64px',
          height: '64px',
          borderRadius: 'var(--radius-full)',
          background: 'var(--danger-light)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'var(--danger)'
        }}>
          <AlertCircle size={32} />
        </div>
        
        <div>
          <h1 style={{
            fontSize: '4rem',
            fontWeight: 800,
            lineHeight: 1,
            color: 'var(--gray-900)',
            marginBottom: '0.5rem'
          }}>404</h1>
          <h2 style={{
            fontSize: 'var(--text-xl)',
            fontWeight: 700,
            color: 'var(--gray-800)',
            marginBottom: '0.75rem'
          }}>Page Not Found</h2>
          <p style={{
            color: 'var(--gray-500)',
            fontSize: 'var(--text-sm)',
            lineHeight: 1.5
          }}>
            The page you are looking for doesn't exist or has been moved. Please verify the URL or return home.
          </p>
        </div>

        <button
          className="btn btn-primary"
          onClick={() => navigate('/dashboard')}
          style={{ width: '100%', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
        >
          <ArrowLeft size={16} />
          <span>Back to Dashboard</span>
        </button>
      </div>
    </div>
  )
}
