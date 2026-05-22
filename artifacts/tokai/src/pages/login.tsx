import { useState } from "react";
import { supabase } from "@/lib/supabase";

type Mode = "signin" | "signup" | "reset";

export default function Login() {
  const [mode, setMode] = useState<Mode>("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);

    if (mode === "signin") {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) setError(error.message);
    } else if (mode === "signup") {
      const { error } = await supabase.auth.signUp({ email, password });
      if (error) setError(error.message);
      else setMessage("Check your email to confirm your account.");
    } else {
      const { error } = await supabase.auth.resetPasswordForEmail(email);
      if (error) setError(error.message);
      else setMessage("Password reset link sent to your email.");
    }

    setLoading(false);
  }

  async function handleGoogle() {
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: window.location.origin, queryParams: { prompt: "select_account" } },
    });
  }

  const inputStyle: React.CSSProperties = {
    width: "100%", padding: "10px 14px", background: "rgba(0,0,0,0.3)",
    border: "1px solid rgba(192,132,252,0.25)", borderRadius: 6,
    color: "#d0e8f8", fontFamily: "'Rajdhani', sans-serif", fontSize: 16,
    outline: "none", boxSizing: "border-box",
  };

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg, #0c0818 0%, #100a25 50%, #080614 100%)", display: "flex", alignItems: "center", justifyContent: "center", padding: 24, fontFamily: "'Rajdhani', sans-serif" }}>
      <div style={{ width: "100%", maxWidth: 400, background: "linear-gradient(135deg, #120d28, #160f30)", border: "1px solid rgba(192,132,252,0.3)", borderRadius: 14, padding: 32, display: "flex", flexDirection: "column", gap: 20, boxShadow: "0 0 60px rgba(192,132,252,0.08)" }}>

        <div style={{ textAlign: "center" }}>
          <div style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 36, letterSpacing: 10 }}>
            <span style={{ color: "#7c3aed" }}>TOK</span><span style={{ color: "#c084fc" }}>AI</span>
          </div>
          <div style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 11, color: "#5a8fa8", letterSpacing: 2, marginTop: 6 }}>
            {mode === "signin" ? "SIGN IN TO YOUR ACCOUNT" : mode === "signup" ? "CREATE ACCOUNT" : "RESET PASSWORD"}
          </div>
        </div>

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <input
            type="email" placeholder="Email address" value={email}
            onChange={e => setEmail(e.target.value)} required style={inputStyle}
          />
          {mode !== "reset" && (
            <input
              type="password" placeholder="Password" value={password}
              onChange={e => setPassword(e.target.value)} required style={inputStyle}
            />
          )}
          {error && (
            <div style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 12, color: "#f87171", letterSpacing: 0.5 }}>
              {error}
            </div>
          )}
          {message && (
            <div style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 12, color: "#6ee7b7", letterSpacing: 0.5 }}>
              {message}
            </div>
          )}
          <button type="submit" disabled={loading}
            style={{ padding: "11px 0", background: loading ? "rgba(192,132,252,0.08)" : "rgba(192,132,252,0.18)", border: "1px solid rgba(192,132,252,0.5)", borderRadius: 6, color: "#c084fc", fontFamily: "'Share Tech Mono', monospace", fontSize: 13, letterSpacing: 2, cursor: loading ? "default" : "pointer", transition: "background 0.2s" }}>
            {loading ? "..." : mode === "signin" ? "SIGN IN" : mode === "signup" ? "CREATE ACCOUNT" : "SEND RESET LINK"}
          </button>
        </form>

        {mode !== "reset" && (
          <>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <div style={{ flex: 1, height: 1, background: "rgba(192,132,252,0.15)" }} />
              <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 10, color: "rgba(90,143,168,0.5)", letterSpacing: 1 }}>OR</span>
              <div style={{ flex: 1, height: 1, background: "rgba(192,132,252,0.15)" }} />
            </div>
            <button onClick={handleGoogle}
              style={{ padding: "11px 0", background: "transparent", border: "1px solid rgba(192,132,252,0.2)", borderRadius: 6, color: "#c8d8e8", fontFamily: "'Share Tech Mono', monospace", fontSize: 13, letterSpacing: 1, cursor: "pointer", transition: "border-color 0.2s", display: "flex", alignItems: "center", justifyContent: "center", gap: 10 }}
              onMouseEnter={e => (e.currentTarget.style.borderColor = "rgba(192,132,252,0.45)")}
              onMouseLeave={e => (e.currentTarget.style.borderColor = "rgba(192,132,252,0.2)")}>
              <svg width="18" height="18" viewBox="0 0 48 48" style={{ flexShrink: 0 }}>
                <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                <path fill="none" d="M0 0h48v48H0z"/>
              </svg>
              Continue with Google
            </button>
          </>
        )}

        <div style={{ display: "flex", justifyContent: "center", gap: 24, flexWrap: "wrap" }}>
          {mode !== "signin" && (
            <span onClick={() => { setMode("signin"); setError(null); setMessage(null); }}
              style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 11, color: "rgba(90,143,168,0.6)", cursor: "pointer", letterSpacing: 0.5 }}
              onMouseEnter={e => (e.currentTarget.style.color = "#c084fc")}
              onMouseLeave={e => (e.currentTarget.style.color = "rgba(90,143,168,0.6)")}>
              Sign in
            </span>
          )}
          {mode !== "signup" && (
            <span onClick={() => { setMode("signup"); setError(null); setMessage(null); }}
              style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 11, color: "rgba(90,143,168,0.6)", cursor: "pointer", letterSpacing: 0.5 }}
              onMouseEnter={e => (e.currentTarget.style.color = "#c084fc")}
              onMouseLeave={e => (e.currentTarget.style.color = "rgba(90,143,168,0.6)")}>
              Create account
            </span>
          )}
          {mode !== "reset" && (
            <span onClick={() => { setMode("reset"); setError(null); setMessage(null); }}
              style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: 11, color: "rgba(90,143,168,0.6)", cursor: "pointer", letterSpacing: 0.5 }}
              onMouseEnter={e => (e.currentTarget.style.color = "#c084fc")}
              onMouseLeave={e => (e.currentTarget.style.color = "rgba(90,143,168,0.6)")}>
              Forgot password
            </span>
          )}
        </div>

      </div>
    </div>
  );
}
