"use client";
import { useState, useEffect } from 'react';

interface SymptomSelectorProps {
  symptoms: string[];
  selectedSymptoms: string[];
  onChange: (symptoms: string[]) => void;
}

export default function SymptomSelector({ symptoms, selectedSymptoms, onChange }: SymptomSelectorProps) {
  const [query, setQuery] = useState('');
  const [filteredSymptoms, setFilteredSymptoms] = useState<string[]>([]);

  useEffect(() => {
    setFilteredSymptoms(
      symptoms.filter((s) => s.toLowerCase().includes(query.toLowerCase()) && !selectedSymptoms.includes(s))
    );
  }, [query, symptoms, selectedSymptoms]);

  const addSymptom = (symptom: string) => {
    onChange([...selectedSymptoms, symptom]);
    setQuery('');
  };

  const removeSymptom = (symptom: string) => {
    onChange(selectedSymptoms.filter((s) => s !== symptom));
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">Select Symptoms</label>
        <div className="flex flex-wrap gap-2 mb-2">
          {selectedSymptoms.map((s) => (
            <span key={s} className="bg-blue-100 text-blue-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded flex items-center">
              {s}
              <button onClick={() => removeSymptom(s)} className="ml-1 text-blue-600 hover:text-blue-800">
                &times;
              </button>
            </span>
          ))}
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type to search symptoms..."
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
        {query && (
          <ul className="bg-white border border-gray-100 mt-1 max-h-40 overflow-y-auto shadow-lg rounded-md absolute z-10 w-full max-w-md">
            {filteredSymptoms.map((s) => (
              <li
                key={s}
                onClick={() => addSymptom(s)}
                className="px-4 py-2 hover:bg-blue-50 cursor-pointer text-gray-700"
              >
                {s}
              </li>
            ))}
            {filteredSymptoms.length === 0 && (
              <li className="px-4 py-2 text-gray-500">No matching symptoms found</li>
            )}
          </ul>
        )}
      </div>
    </div>
  );
}
