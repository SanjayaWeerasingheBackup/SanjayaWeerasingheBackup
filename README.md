import { useState, useEffect, useCallback } from 'react';

const MatrixGame = () => {
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [position, setPosition] = useState(50);
  const [obstacles, setObstacles] = useState([]);
  
  const handleKeyPress = useCallback((e) => {
    if (e.key === 'ArrowLeft' && position > 0) {
      setPosition(p => Math.max(0, p - 5));
    }
    if (e.key === 'ArrowRight' && position < 90) {
      setPosition(p => Math.min(90, p + 5));
    }
  }, [position]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [handleKeyPress]);

  useEffect(() => {
    if (gameOver) return;

    const gameLoop = setInterval(() => {
      setObstacles(prev => {
        const newObstacles = prev
          .map(obs => ({ ...obs, y: obs.y + 2 }))
          .filter(obs => obs.y < 100);

        if (Math.random() < 0.05) {
          newObstacles.push({
            x: Math.random() * 90,
            y: -10,
            type: Math.random() < 0.3 ? 'bonus' : 'obstacle'
          });
        }

        // Collision detection
        newObstacles.forEach(obs => {
          if (obs.y > 80 && obs.y < 90 &&
              Math.abs(obs.x - position) < 5) {
            if (obs.type === 'bonus') {
              setScore(s => s + 10);
            } else {
              setGameOver(true);
            }
          }
        });

        return newObstacles;
      });

      setScore(s => s + 1);
    }, 50);

    return () => clearInterval(gameLoop);
  }, [position, gameOver]);

  return (
    <div className="relative w-full h-96 bg-black overflow-hidden font-mono text-green-500 border border-green-500">
      <div className="absolute top-2 right-2">Score: {score}</div>
      
      {/* Player */}
      <div 
        className="absolute bottom-4 w-4 h-4 bg-green-500"
        style={{ left: `${position}%` }}
      >▲</div>

      {/* Obstacles */}
      {obstacles.map((obs, i) => (
        <div
          key={i}
          className={`absolute w-3 h-3 ${obs.type === 'bonus' ? 'text-yellow-500' : 'text-red-500'}`}
          style={{ left: `${obs.x}%`, top: `${obs.y}%` }}
        >
          {obs.type === 'bonus' ? '$' : 'X'}
        </div>
      ))}

      {/* Matrix rain effect */}
      <div className="absolute inset-0 pointer-events-none opacity-20">
        {Array.from({ length: 20 }).map((_, i) => (
          <div
            key={i}
            className="absolute animate-fall text-sm"
            style={{
              left: `${i * 5}%`,
              animationDelay: `${Math.random() * 2}s`
            }}
          >
            {Array.from({ length: 10 }).map((_, j) => (
              <div key={j}>{String.fromCharCode(0x30A0 + Math.random() * 96)}</div>
            ))}
          </div>
        ))}
      </div>

      {/* Game Over Screen */}
      {gameOver && (
        <div className="absolute inset-0 bg-black bg-opacity-80 flex items-center justify-center flex-col">
          <div className="text-2xl mb-4">GAME OVER</div>
          <div className="mb-4">Final Score: {score}</div>
          <button
            onClick={() => {
              setGameOver(false);
              setScore(0);
              setObstacles([]);
            }}
            className="px-4 py-2 border border-green-500 hover:bg-green-500 hover:text-black transition-colors"
          >
            RETRY
          </button>
        </div>
      )}
    </div>
  );
};

export default MatrixGame;
