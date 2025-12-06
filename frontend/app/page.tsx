"use client";
import { useState, useEffect } from 'react';
import SymptomSelector from '../components/SymptomSelector';
import ResultCard from '../components/ResultCard';

export default function Home() {
  const [allSymptoms, setAllSymptoms] = useState<string[]>([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // In production (Vercel), use relative path (empty string) to hit the same domain's /api routes.
  // Locally, point to the Flask server on port 5000.
  const API_URL = process.env.NEXT_PUBLIC_API_URL || (process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000');

  useEffect(() => {
    fetch(`${API_URL}/api/symptoms`)
      .then((res) => res.json())
      .then((data) => setAllSymptoms(data.symptoms))
      .catch((err) => console.error('Failed to fetch symptoms', err));
  }, []);

  const handlePredict = async () => {
    if (selectedSymptoms.length === 0) {
      setError('Please select at least one symptom.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms: selectedSymptoms }),
      });
      const data = await res.json();
      if (res.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Prediction failed');
      }
    } catch (err) {
      setError('Failed to connect to the server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            AI Health Assistant
          </h1>
          <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
            Select your symptoms and get instant AI-powered disease predictions and health recommendations.
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-xl overflow-hidden mb-10 p-8">
          <SymptomSelector
            symptoms={allSymptoms}
            selectedSymptoms={selectedSymptoms}
            onChange={setSelectedSymptoms}
          />

          {error && (
            <div className="mt-4 p-4 bg-red-100 text-red-700 rounded-md">
              {error}
            </div>
          )}

          <div className="mt-6 flex justify-center">
            <button
              onClick={handlePredict}
              disabled={loading}
              className="px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10 transition-colors disabled:opacity-50"
            >
              {loading ? 'Analyzing...' : 'Predict Disease'}
            </button>
          </div>
        </div>

        {result && (
          <div className="space-y-8 animate-fade-in">
            <div className="bg-white rounded-xl shadow-xl p-8 text-center border-l-4 border-indigo-500">
              <h2 className="text-2xl font-bold text-gray-900">Predicted Disease</h2>
              <p className="text-4xl font-extrabold text-indigo-600 mt-2">{result.disease}</p>
              <p className="mt-4 text-gray-600">{result.description}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <ResultCard title="Precautions" content={result.precautions} color="bg-blue-500" />
              <ResultCard title="Medications" content={result.medications} color="bg-green-500" />
              <ResultCard title="Diet" content={result.diet} color="bg-yellow-500" />
              <ResultCard title="Workout" content={result.workout} color="bg-red-500" />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
