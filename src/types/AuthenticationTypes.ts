interface SignUpFormType {
  name: string;
  username: string;
  password: string;
}

interface SignUpResponseType {
  date_joined: string
  email: string
  first_name: string
  groups: string[] | number[]
  id: number
  is_active: boolean
  is_staff: boolean
  is_superuser: boolean
  last_login: null
  last_name: string
  name: string
  user_permissions: string[] | number[]
  username: string
}

interface SignInFormType {
  username: string;
  password: string;
}

interface SignInResponseType {
  refresh: string,
  access: string,
}

export type {SignUpFormType, SignUpResponseType, SignInFormType, SignInResponseType};