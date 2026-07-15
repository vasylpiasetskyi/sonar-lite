interface LoadingStateProps {
  label?: string
}

function LoadingState({ label = 'Loading...' }: LoadingStateProps) {
  return <div className="flex items-center justify-center p-6 text-sm text-slate-500">{label}</div>
}

export default LoadingState
