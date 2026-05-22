import { useState, useEffect } from "react";
import type { Session } from "@supabase/supabase-js";
import { supabase } from "@/lib/supabase";
import Dashboard from "@/pages/dashboard";
import Login from "@/pages/login";

export default function App() {
  const [session, setSession] = useState<Session | null | undefined>(undefined);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setSession(data.session));
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });
    return () => subscription.unsubscribe();
  }, []);

  if (session === undefined) return (
    <div style={{ minHeight: "100vh", background: "#0c0818", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "'Share Tech Mono', monospace", fontSize: 13, color: "#5a8fa8", letterSpacing: 2 }}>
      LOADING...
    </div>
  );
  if (!session) return <Login />;
  return <Dashboard session={session} />;
}
