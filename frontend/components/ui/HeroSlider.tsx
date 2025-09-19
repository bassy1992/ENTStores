import { useEffect, useState } from 'react';

export default function HeroSlider({ images }: { images: string[] }) {
  const [idx, setIdx] = useState(0);

  useEffect(() => {
    if (!images || images.length <= 1) return;
    const t = setInterval(() => setIdx((i) => (i + 1) % images.length), 4000);
    return () => clearInterval(t);
  }, [images]);

  if (!images || images.length === 0) return null;

  return (
    <div className="relative rounded-2xl overflow-hidden">
      {images.map((src, i) => (
        <img
          key={src}
          src={src}
          alt={`slide-${i}`}
          className={`w-full h-80 sm:h-[420px] object-cover transition-opacity duration-700 ${i === idx ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
        />
      ))}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
        {images.map((_, i) => (
          <button
            key={i}
            onClick={() => setIdx(i)}
            className={`h-2 w-8 rounded-full ${i === idx ? 'bg-white' : 'bg-white/40'}`}
          />
        ))}
      </div>
    </div>
  );
}
