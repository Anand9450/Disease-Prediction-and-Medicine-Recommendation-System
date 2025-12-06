interface ResultCardProps {
  title: string;
  content: string | string[];
  color: string;
}

export default function ResultCard({ title, content, color }: ResultCardProps) {
  return (
    <div className={`p-6 rounded-lg shadow-md text-white ${color} transition-transform hover:scale-105`}>
      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <div className="text-sm">
        {Array.isArray(content) ? (
          <ul className="list-disc list-inside">
            {content.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        ) : (
          <p>{content}</p>
        )}
      </div>
    </div>
  );
}
