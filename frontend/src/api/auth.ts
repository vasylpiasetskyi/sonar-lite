import { useMutation } from '@tanstack/react-query'

import { apiPost, setAuthToken } from './client'
import type { AuthResponse } from './types'

interface Credentials {
  email: string
  password: string
}

export function useRegister() {
  return useMutation({
    mutationFn: (credentials: Credentials) =>
      apiPost<AuthResponse>('/auth/register', credentials),
    onSuccess: (data) => setAuthToken(data.access_token),
  })
}

export function useLogin() {
  return useMutation({
    mutationFn: (credentials: Credentials) => apiPost<AuthResponse>('/auth/login', credentials),
    onSuccess: (data) => setAuthToken(data.access_token),
  })
}
