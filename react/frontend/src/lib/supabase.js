import { createClient } from '@supabase/supabase-js'

// Replace these with your Supabase project URL and anon key
const supabaseUrl = process.env.VITE_SUPABASE_URL
const supabaseAnonKey = process.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey) 