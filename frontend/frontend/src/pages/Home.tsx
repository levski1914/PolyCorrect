import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";

type Issue = {
  type: string;
  adj: string;
  noun: string;
  adj_gender?: string;
  noun_gender?: string;
  adj_number?: string;
  noun_number?: string;
};

type ResponseData = {
  original_text: string;
  issues: Issue[];
};

export default function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<ResponseData | null>(null);

  const handleAnalyze = async () => {
    const {
      data: { session },
    } = await supabase.auth.getSession();

    const token = session?.access_token;

    if (!token) {
      alert("Моля, влез в акаунта си.");
      return;
    }

    const res = await fetch("http://localhost:8000/analyze-and-save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ content: text }),
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="p-6 max-w-xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">PolyCorrect</h1>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full h-40 border p-2 rounded"
        placeholder="Въведи текст за проверка..."
      />
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={handleAnalyze}
      >
        Провери и запази
      </button>

      {result && (
        <div className="mt-4 bg-gray-100 p-4 rounded">
          <p className="font-semibold">Открити грешки:</p>
          {result.issues.length === 0 ? (
            <p>Няма грешки 🎉</p>
          ) : (
            <ul className="list-disc pl-5">
              {result.issues.map((issue, i) => (
                <li key={i}>
                  {issue.type}: <b>{issue.adj}</b> → <b>{issue.noun}</b>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
