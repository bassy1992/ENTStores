import { useState, useCallback } from 'react';

export default function HeroCarousel({ images }: { images: string[] }) {
  const [index, setIndex] = useState(0);
  const len = images?.length || 0;

  const prev = useCallback(() => setIndex((i) => (i - 1 + len) % len), [len]);
  const next = useCallback(() => setIndex((i) => (i + 1) % len), [len]);

  if (!images || images.length === 0) return null;

  return (
    <div className="relative rounded-2xl overflow-hidden">
      <div className="relative">
        {images.map((src, i) => (
          <img
            key={src}
            src={src}
            alt={`slide-${i}`}
            className={`w-full h-80 sm:h-[420px] object-cover transition-opacity duration-300 ${i === index ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
          />
        ))}

        {/* Left / Right controls */}
        <button
          onClick={prev}
          aria-label="Previous"
          className="absolute left-3 top-1/2 -translate-y-1/2 rounded-full bg-white/80 p-2 shadow hover:bg-white"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-black" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M12.293 16.293a1 1 0 010-1.414L15.586 11H5a1 1 0 110-2h10.586l-3.293-3.293a1 1 0 111.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clipRule="evenodd" transform="rotate(180 10 8)"/>
          </svg>
        </button>

        <button
          onClick={next}
          aria-label="Next"
          className="absolute right-3 top-1/2 -translate-y-1/2 rounded-full bg-white/80 p-2 shadow hover:bg-white"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-black" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M12.293 16.293a1 1 0 010-1.414L15.586 11H5a1 1 0 110-2h10.586l-3.293-3.293a1 1 0 111.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clipRule="evenodd" />
          </svg>
        </button>

        {/* Indicators */}
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
          {images.map((_, i) => (
            <button
              key={i}
              onClick={() => setIndex(i)}
              aria-label={`Go to slide ${i + 1}`}
              className={`h-2 w-8 rounded-full ${i === index ? 'bg-white' : 'bg-white/40'}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
