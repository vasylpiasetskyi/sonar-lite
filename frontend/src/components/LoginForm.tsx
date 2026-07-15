import { useState } from 'react'
import { useForm } from 'react-hook-form'

import { useLogin, useRegister } from '../api/auth'
import ErrorState from './ErrorState'

interface LoginFormValues {
  email: string
  password: string
}

interface LoginFormProps {
  onAuthenticated: () => void
}

function LoginForm({ onAuthenticated }: LoginFormProps) {
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const { register: registerField, handleSubmit } = useForm<LoginFormValues>()
  const login = useLogin()
  const register = useRegister()

  const activeMutation = mode === 'login' ? login : register

  const onSubmit = handleSubmit((values) => {
    activeMutation.mutate(values, { onSuccess: () => onAuthenticated() })
  })

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 p-6">
      <form
        onSubmit={onSubmit}
        className="w-full max-w-sm space-y-4 rounded-lg bg-white p-6 shadow"
      >
        <h1 className="text-xl font-bold text-slate-900">Sonar Lite</h1>
        <div className="flex gap-2 text-sm">
          <button
            type="button"
            onClick={() => setMode('login')}
            className={mode === 'login' ? 'font-semibold text-blue-600' : 'text-slate-400'}
          >
            Log in
          </button>
          <span className="text-slate-300">/</span>
          <button
            type="button"
            onClick={() => setMode('register')}
            className={mode === 'register' ? 'font-semibold text-blue-600' : 'text-slate-400'}
          >
            Register
          </button>
        </div>

        <label className="block text-xs text-slate-500">
          Email
          <input
            type="email"
            className="mt-1 w-full rounded border border-slate-300 p-2 text-sm"
            {...registerField('email', { required: true })}
          />
        </label>
        <label className="block text-xs text-slate-500">
          Password
          <input
            type="password"
            className="mt-1 w-full rounded border border-slate-300 p-2 text-sm"
            {...registerField('password', { required: true, minLength: 8 })}
          />
        </label>

        <button
          type="submit"
          disabled={activeMutation.isPending}
          className="w-full rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          {activeMutation.isPending ? 'Please wait...' : mode === 'login' ? 'Log in' : 'Register'}
        </button>

        {activeMutation.isError && (
          <ErrorState message="Invalid email or password, or the email is already registered." />
        )}
      </form>
    </div>
  )
}

export default LoginForm
