import React, { useState } from "react";
import axios from "axios";

type Issue = {
  type: string;
  adj: string;
  noun: string;
  adj_gender?: string;
  noun_gender?: string;
  adj_number?: string;
  noun_number?: string;
};

type AnalysisResponse = {
  original_text: string;
  issues: Issue[];
};
type Props = {};

const Home = (props: Props) => {
  const [text, setText] = useState("");
  const [result, setResult] = useState<AnalysisResponse | null>(null);

  const checkText = async () => {
    try {
      const res = await axios.post<AnalysisResponse>(
        "http://localhost:8000/analyze-and-save",
        { content: text }
      );
      setResult(res.data);
    } catch (err) {
      console.error("Грешка при анализа:", err);
    }
  };
  return (
    <div className="p-8 max-w-xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">PolyCorrect</h1>
      <textarea
        className="w-full h-40 border rounded p-2"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Въведи текст за проверка..."
      />
      <button
        onClick={checkText}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Провери и запази
      </button>

      {result && (
        <div className="mt-4 bg-gray-100 p-4 rounded">
          <p className="font-semibold">Открити проблеми:</p>
          {result.issues.length === 0 ? (
            <p>Няма грешки 🎉</p>
          ) : (
            <ul className="list-disc pl-6">
              {result.issues.map((issue, idx) => (
                <li key={idx}>
                  {issue.type}: <b>{issue.adj}</b> → <b>{issue.noun}</b>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default Home;
