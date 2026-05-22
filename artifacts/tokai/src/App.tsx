import { useState, useEffect } from "react";
import type { Session } from "@supabase/supabase-js";
import { supabase } from "@/lib/supabase";
import Dashboard from "@/pages/dashboard";
import Login from "@/pages/login";

const inputStyle: React.CSSProperties = {
  width: "100%", padding: "10px 14px", background: "rgba(0,0,0,0.3)",
  border: "1px solid rgba(192,132,252,0.25)", borderRadius: 6,
  color: "#d0e8f8", fontFamily: "'Rajdhani', sans-serif", fontSize: 16,
  outline: "none", boxSizing: "border-box",
};

function ResetPassword() {
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (password !== confirm) { setError("Passwords do not match."); return; }
    if (password.length < 6) { setError("Password must be at least 6 characters."); return; }
    setLoading(true);
    setError(null);
    const { error } = await supabase.auth.updateUser({ password });
    if (error) { setError(error.message); setLoading(false); return; }
    setDone(true);
    setLoading(false);
    setTimeout(() => supabase.auth.signOut(), 2000);
  }

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg, #0c0818 0%, #100a25 50%, #080614 100%)", display: "flex", alignItems: "center", justifyContent: "center", padding: 24, fontFamily: "'Rajdhani', sans-serif" }}>
      <div style={{ width: "100%", maxWidth: 400, background: "linear-gradient(135deg, #120d28, #160f30)", border: "1px solid rgba(192,132,252,0.3)", borderRadius: 14, padding: 32, display: "flex", flexDirection: "column", gap: 20, boxShadow: "0 0 60px rgba(192,132,252,0.08)" }}>
        <div style={{ textAlign: "center" }}>
          <div style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 36, letterSpacing: 10 }}>
            <span style={{ color: "#7c3aed" }}>TOK</span><span style={{ color: "#c084fc" }}>AI</span>
          </div>
          <div style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 11, color: "#5a8fa8", letterSpacing: 2, marginTop: 6 }}>
            SET NEW PASSWORD
          </div>
        </div>

        {done ? (
          <div style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 12, color: "#6ee7b7", letterSpacing: 0.5, textAlign: "center" }}>
            Password updated. You can close this tab and sign in.
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <input type="password" placeholder="New password" value={password}
              onChange={e => setPassword(e.target.value)} required style={inputStyle} />
            <input type="password" placeholder="Confirm new password" value={confirm}
              onChange={e => setConfirm(e.target.value)} required style={inputStyle} />
            {error && (
              <div style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 12, color: "#f87171", letterSpacing: 0.5 }}>
                {error}
              </div>
            )}
            <button type="submit" disabled={loading}
              style={{ padding: "11px 0", background: loading ? "rgba(192,132,252,0.08)" : "rgba(192,132,252,0.18)", border: "1px solid rgba(192,132,252,0.5)", borderRadius: 6, color: "#c084fc", fontFamily: "'Share Tech Mono', monospace", fontSize: 13, letterSpacing: 2, cursor: loading ? "default" : "pointer" }}>
              {loading ? "..." : "UPDATE PASSWORD"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default function App() {
  const [session, setSession] = useState<Session | null | undefined>(undefined);
  const [recovering, setRecovering] = useState(() =>
    window.location.hash.includes("type=recovery")
  );

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setSession(data.session));
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      if (event === "PASSWORD_RECOVERY") setRecovering(true);
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
  if (recovering) return <ResetPassword />;
  return <Dashboard session={session} />;
}
