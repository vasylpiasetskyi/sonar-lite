interface EmptyStateProps {
  message: string
}

function EmptyState({ message }: EmptyStateProps) {
  return (
    <div className="rounded-md border border-dashed border-slate-300 p-4 text-center text-sm text-slate-500">
      {message}
    </div>
  )
}

export default EmptyState
