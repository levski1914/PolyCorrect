import { createClient } from "@supabase/supabase-js";
const supabaseUrl = "https://uwjgaqhmsvinsagqnxkg.supabase.co";
const supaBaseAnonKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3amdhcWhtc3ZpbnNhZ3FueGtnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5MzIwNDAsImV4cCI6MjA2MzUwODA0MH0.XU2C416UWjDCyf68-YEmQMJFp9tlH5gp1DSuHIU_qEU";

export const supabase = createClient(supabaseUrl, supaBaseAnonKey);
